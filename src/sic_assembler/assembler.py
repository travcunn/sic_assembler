from collections import namedtuple

import fuckit

from errors import DuplicateSymbolError, LineFieldsError, OpcodeLookupError
from instructions import flag_table, op_table


__all__ = ['assemble']

LineFields = namedtuple('LineFields', 'label opcode operand')


class Format1(object):
    """ Format 1 template class. """
    def __init__(self, symtab, opcode, address):
        self._symtab = symtab
        self._opcode = opcode
        self._address = address

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._opcode is None:
            raise LineFieldsError(message="An opcode was not specified.")

        output = ""

        # lookup the opcode
        opcode_lookup = op_table[self._opcode].opcode
        stripped_opcode = str(hex(opcode_lookup)).lstrip("0x") or "0"
        padded_opcode = stripped_opcode.zfill(2)
        output += str(padded_opcode)

        # look up the address in symtab
        if self._address is not None:
            symtab_lookup = self._symtab[self._address]
            stripped_address = str(symtab_lookup).lstrip("0x") or "0"
            padded_address = stripped_address.zfill(4)
            output += str(padded_address)
            #output += str(self._symtab[self._address])
        else:
            output += "0000"

        return self._opcode, self._address, output


def assemble(inputfile, verbosity=0):
    """ Assemble the contents of a file-like object. """
    contents = (line.rstrip('\n') for line in inputfile.readlines())

    # Temporary array to store results of the first pass
    temp_contents = []

    # Symbol table
    symtab = dict()
    # Location counter
    locctr = 0
    # Starting address
    start_address = 0
    # Program length
    program_length = 0

    # Define a comment
    comment = lambda x: x.split()[0].startswith('.')
    # Define a blank line
    blank_line = lambda x: len(x.split()) == 0

    """ Pass 1. """

    # Read the first line and search for 'START'
    first = contents.next()
    first_line = parse_line(first, 1)
    if first_line.opcode is not None:
        # If the opcode is 'START', set the locctr to the starting address
        if first_line.opcode == 'START':
            start_address = int(first_line.operand, 16)
            locctr = int(first_line.operand, 16)

    # Loop through every line excluding the first
    for line_number, line in enumerate(contents):
        if not blank_line(line) and not comment(line):
            line_fields = parse_line(line, line_number)

            # If there is a label, search for it, and/or add it to symtab
            if line_fields.label is not None:
                if line_fields.label not in symtab:
                    symtab[line_fields.label] = hex(locctr)
                else:
                    raise DuplicateSymbolError(
                            message="""A duplicate symbol was found on line:
                            """ + str(line_number+1), code=1,
                            line_number=line_number+1, contents=line)

            # Search optab for the opcode
            if line_fields.opcode in op_table:
                locctr += 3
            elif line_fields.opcode == 'WORD':
                locctr += 3
            elif line_fields.opcode == 'RESW':
                locctr += 3 * int(line_fields.operand)
            elif line_fields.opcode == 'RESB':
                locctr += int(line_fields.operand)
            elif line_fields.opcode == 'BYTE':
                locctr += len(line_fields.operand)
                pass
            elif line_fields.opcode == 'END':
                # Stop reading through the file contents
                break
            else:
                raise OpcodeLookupError(message='The opcode is invalid on line:' +
                                  str(line_number+1), code=1,
                                  line_number=line_number+1, contents=line)

            # Add to the temporary array
            temp_contents.append(line)

    """ Pass 2. """

    for line_number, line in enumerate(temp_contents):
        line_fields = parse_line(line, line_number)
        # Generate an instruction
        if line_fields.opcode == 'WORD':
            pass
        elif line_fields.opcode == 'RESW':
            pass
        elif line_fields.opcode == 'RESB':
            pass
        elif line_fields.opcode == 'BYTE':
            pass
        else:
            instruction = Format1(symtab=symtab, opcode=line_fields.opcode,
                                  address=line_fields.operand)

            print instruction.generate()


    ####################### DEBUG #########################
    program_length = locctr - start_address
    print "Program length (decimal):", program_length
    print "Program length (hex):", hex(program_length)

    target = 0x107a
    print "Target length (decimal):", target
    print "Target length (hex):", hex(target)
    if (program_length - target) is not 0:
        print "ERROR: THE PROGRAM LENGTH IS OFF BY:", program_length - target

    print symtab


def parse_line(line, line_number):
    """ Parse an individual line and return a namedtuple of the contents. """
    fields = line.split()
    if len(fields) is 3:
        return LineFields(label=fields[0], opcode=fields[1], operand=fields[2])
    elif len(fields) is 2:
        return LineFields(label=None, opcode=fields[0], operand=fields[1])
    elif len(fields) is 1:
        return LineFields(label=None, opcode=fields[0], operand=None)
    else:
        raise LineFieldsError(message='Invalid amount of fields on line:' +
                              str(line_number+1), code=1,
                              line_number=line_number+1, contents=line)
