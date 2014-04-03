from errors import DuplicateSymbolError, LineFieldsError, OpcodeLookupError, \
        UndefinedSymbolError
from instructions import op_table, registers_table


# A comment
comment = lambda x: x.split()[0].startswith('.')
# A blank line
blank_line = lambda x: len(x.split()) == 0

# Indexed addressing
indexed = lambda x: x.endswith(',X')
# Indirect addressing
indirect = lambda x: x.startswith('@')
# An immediate operand
immediate = lambda x: x.startswith('#')
# An extended format instruction
extended = lambda x: x.startswith('+')
# Literal
literal = lambda x: x.startswith('=')


class SourceLine(object):
    def __init__(self, label, opcode, operand):
        self.label = label
        self.opcode = opcode
        self.operand = operand


class Format(object):
    """ Base Instruction Format class. """
    def generate(self):
        raise NotImplementedError


class Format1(Format):
    """ Format 1 instruction class.

         8
     ==========
    |    op    |
     ==========

    """
    def __init__(self, opcode):
        self._opcode = opcode

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

        return self._opcode, None, output


class Format2(Format):
    """ Format 2 instruction class.

         8       4     4
     ======================
    |    op    | r1 |  r2  |
     ======================

    """
    def __init__(self, opcode, r1, r2):
        self._opcode = opcode
        self._r1 = r1
        self._r2 = r2

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

        # look up the registers
        r1_lookup = registers_table[self._r1]
        stripped_r1 = str(hex(r1_lookup)).lstrip("0x") or "0"
        output += str(stripped_r1)

        if self._r2 is not None:
            r2_lookup = registers_table[self._r2]
            stripped_r2 = str(hex(r2_lookup)).lstrip("0x") or "0"
            output += str(stripped_r2)
        else:
            output += "0"

        return self._opcode, (self._r1, self._r2), output

#TODO: make this work correctly, with flags
class Format3(Format):
    """ Format 3 instruction class.

        6      1   1   1   1   1   1         12
     =================================================
    |   op   | n | i | x | b | p | e |      disp      |
     =================================================

    """
    def __init__(self, flags, opcode, disp):
        self._opcode = opcode
        self._disp = disp

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
        if self._disp is not None:
            stripped_address = str(self._disp).lstrip("0x") or "0"
            padded_address = stripped_address.zfill(4)
            output += str(padded_address)
        else:
            output += "0000"

        return self._opcode, self._disp, output


#TODO: make this work correctly, with flags
class Format4(Format):
    """ Format 4 instruction class.

        6      1   1   1   1   1   1              20
     ============================================================
    |   op   | n | i | x | b | p | e |          address          |
     ============================================================

    """
    def __init__(self, flags, line_info):
        self._symtab = line_info['symtab']
        self._opcode = line_info['opcode']
        self._address = line_info['operand']

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
            stripped_address = str(self._address).lstrip("0x") or "0"
            padded_address = stripped_address.zfill(4)
            output += str(padded_address)
            #output += str(self._symtab[self._address])
        else:
            output += "0000"

        return self._opcode, self._address, output


class Assembler(object):
    def __init__(self, inputfile, verbosity=0):
        self.verbosity = verbosity

        self.contents = (line.rstrip('\n') for line in inputfile.readlines())
        # Temporary array to store results of the first pass
        self.temp_contents = []
        # Symbol table
        self.symtab = dict()
        # Location counter
        self.locctr = 0
        # Starting address
        self.start_address = 0
        # Program length
        self.program_length = 0

        # array of tuples containing debugging information
        self.generated_objects = []

    def assemble(self):
        """ Assemble the contents of a file-like object. """
        self.first_pass()
        self.second_pass()

    def first_pass(self):
        """ Pass 1. """

        # Read the first line and search for 'START'
        first = self.contents.next()
        first_line = parse_line(first, 1)
        if first_line.opcode is not None:
            # If the opcode is 'START', set the locctr to the starting address
            if first_line.opcode == 'START':
                self.start_address = int(first_line.operand, 16)
                self.locctr = int(first_line.operand, 16)

        # Loop through every line excluding the first
        for line_number, line in enumerate(self.contents):
            if not blank_line(line) and not comment(line):
                line_fields = parse_line(line, line_number)

                # If there is a label, search for it, and/or add it to symtab
                if line_fields.label is not None:
                    if line_fields.label not in self.symtab:
                        self.symtab[line_fields.label] = hex(self.locctr)
                    else:
                        raise DuplicateSymbolError(
                                message="A duplicate symbol was found on line: " +
                                str(line_number+2), code=1,
                                line_number=line_number+2, contents=line)

                # Search optab for the opcode
                if line_fields.opcode in op_table:
                    self.locctr += 3
                elif line_fields.opcode == 'WORD':
                    self.locctr += 3
                elif line_fields.opcode == 'RESW':
                    self.locctr += 3 * int(line_fields.operand)
                elif line_fields.opcode == 'RESB':
                    self.locctr += int(line_fields.operand)
                elif line_fields.opcode == 'BYTE':
                    if line_fields.operand.startswith('X'):
                        value = line_fields.operand.replace("X", '')
                        stripped_value = value.replace("'", '')
                        hex_value = int(stripped_value, 16)
                        self.locctr += (len(hex(hex_value)) - 2) / 2
                    elif line_fields.operand.startswith("C"):
                        value = line_fields.operand.replace("C", '')
                        stripped_value = value.replace("'", '')
                        self.locctr += len(stripped_value)
                    else:
                        raise LineFieldsError(message="Invalid value for BYTE on line: " +
                                str(line_number+2), code=1,
                                line_number=line_number+2, contents=line)
                elif line_fields.opcode == 'END':
                    # Stop reading through the file contents
                    break
                else:
                    raise OpcodeLookupError(message='The opcode is invalid on line: ' +
                                    str(line_number+2), code=1,
                                    line_number=line_number+2, contents=line)

                # Add to the temporary array
                self.temp_contents.append(line)

    def second_pass(self):
        """ Pass 2. """

        object_code = []

        for line_number, line in enumerate(self.temp_contents):
            line_fields = parse_line(line, line_number)
            found_opcode = op_table.get(line_fields.opcode)
            if found_opcode:
                # determine the instruction format
                format = determine_format(line_fields.opcode)
                if line_fields.operand is not None and not \
                        literal(line_fields.operand):
                    if format is 3:  # only lookup symbols if type 3
                        found_symbol_address = self.symtab.get(line_fields.operand)
                        if found_symbol_address is not None:
                            line_fields.operand = found_symbol_address
                        else:
                            line_fields.operand = 0
                            raise UndefinedSymbolError(
                                    message='Undefined symbol on line: ' +
                                    str(line_number+1), code=1,
                                    line_number=line_number+1, contents=line)
                #TODO: process the literal here in an elif
                else:
                    line_fields.operand = 0

                #TODO eventually only have this in format 3 and 4
                # data to be passed into each instruction type
                instruction_info = {'symtab': self.symtab,
                                    'opcode': line_fields.opcode,
                                    'operand': line_fields.operand}

                #TODO: determine which instruction format to create

                if format is 1:
                    instruction = Format1(opcode=line_fields.opcode)
                elif format is 2:
                    expected_operands = op_table[line_fields.opcode].operands
                    if len(expected_operands) == 2:
                        r1, r2 = line_fields.operand.split(',')
                    elif len(expected_operands) == 1:
                        r1, r2 = line_fields.operand, None
                    instruction = Format2(opcode=line_fields.opcode,
                                          r1=r1, r2=r2)
                elif format is 3:
                    instruction = Format3(None, opcode=line_fields.opcode,
                                          disp=line_fields.operand)
                elif format is 4:
                    instruction = Format4(None, instruction_info)

                object_code.append(instruction.generate())

            else:
                if line_fields.opcode == 'WORD':
                    hex_value = hex(int(line_fields.operand))
                    stripped_value = hex_value.lstrip("0x")
                    padded_value = stripped_value.zfill(6)
                    object_info = (line_fields.opcode, line_fields.operand,
                                   padded_value)
                    object_code.append(object_info)
                elif line_fields.opcode == 'BYTE':
                    if line_fields.operand.startswith('X'):
                        value = line_fields.operand.replace("X", '')
                        stripped_value = value.replace("'", '')
                        object_info = (line_fields.opcode,
                                       line_fields.operand, stripped_value)
                        object_code.append(object_info)
                    elif line_fields.operand.startswith("C"):
                        value = line_fields.operand.replace("C", '')
                        stripped_value = value.replace("'", '')
                        hex_value = stripped_value.encode('hex')
                        object_info = (line_fields.opcode,
                                       line_fields.operand, hex_value)
                        object_code.append(object_info)

        self.generated_objects = object_code


def determine_format(opcode):
    """ Determine the instruction format. """
    if extended(opcode):
        return op_table[opcode].format + 1
    else:
        return op_table[opcode].format


def parse_line(line, line_number):
    """ Parse an individual line and return a namedtuple of the contents. """
    fields = line.split()
    if len(fields) is 3:
        return SourceLine(label=fields[0], opcode=fields[1], operand=fields[2])
    elif len(fields) is 2:
        return SourceLine(label=None, opcode=fields[0], operand=fields[1])
    elif len(fields) is 1:
        return SourceLine(label=None, opcode=fields[0], operand=None)
    else:
        raise LineFieldsError(message='Invalid amount of fields on line:' +
                              str(line_number+1), code=1,
                              line_number=line_number+1, contents=line)



def step(message):
    raw_input(message)
