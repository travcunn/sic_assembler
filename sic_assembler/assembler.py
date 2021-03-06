import codecs

from sic_assembler.errors import DuplicateSymbolError, LineFieldsError, OpcodeLookupError
from sic_assembler.instructions import Format
from sic_assembler.instructions import Format1, Format2, Format3, Format4
from sic_assembler.instructions import extended, op_table
from sic_assembler.records import generate_records


# A comment
comment = lambda x: x.split()[0].startswith('.')
# A blank line
blank_line = lambda x: len(x.split()) == 0


def remove_comments(line):
    """
    Search for a string beginning with a comment in a line and remove all
    every element after that element.
    """
    for x, y in enumerate(line):
        if comment(y):
            return line[:x]
    return line


class SourceLine(object):
    def __init__(self, line_number, label, mnemonic, operand):
        self.location = None
        self.line_number = line_number
        self.label = label
        self.mnemonic = mnemonic
        self.operand = operand

    @staticmethod
    def parse(line, line_number):
        """ Parse an individual line and return a SourceLine object. """
        fields = remove_comments(line.split())

        # if there is a space between operands, fix it
        if len(fields) > 1 and fields[1].endswith(','):
            operands = fields.pop(1) + fields.pop(1)
            fields.append(operands)
        elif len(fields) > 2 and fields[2].endswith(','):
            operands = fields.pop(2) + fields.pop(2)
            fields.append(operands)

        if len(fields) is 3:
            return SourceLine(label=fields[0], mnemonic=fields[1],
                              operand=fields[2], line_number=line_number)
        elif len(fields) is 2:
            return SourceLine(label=None, mnemonic=fields[0],
                              operand=fields[1], line_number=line_number)
        elif len(fields) is 1:
            return SourceLine(label=None, mnemonic=fields[0], operand=None,
                              line_number=line_number)
        else:
            raise LineFieldsError(
                    message='Invalid amount of fields on line:' +
                    str(line_number+1), code=1,
                    line_number=line_number+1, contents=line)

    def __repr__(self):
        return "<SourceLine: %s, %s, %s>" % (self.label, self.mnemonic,
                                             self.operand)


class Assembler(object):
    def __init__(self, inputfile, verbosity=0):
        self.verbosity = verbosity

        self.contents = (line.rstrip('\n') for line in inputfile.readlines())
        # Temporary array to store results of the first pass
        self.temp_contents = []
        # Symbol table
        self.symtab = dict()
        # Location counter
        self.locctr = int(0)
        # Starting address
        self.start_address = 0
        # Program length
        self.program_length = 0
        # Program name
        self.program_name = ""
        # BASE register
        self.base = None
        # array of tuples containing debugging information
        self.__generated_objects = []
        # array of the generated records
        self.__generated_records = []

    def assemble(self):
        """ Assemble the contents of a file-like object. """
        if len(self.__generated_records) is 0:
            self.first_pass()
            self.second_pass()
            # Generate some records
            self.__generated_records = self.generate_records()

        return self.generated_records

    def first_pass(self):
        """ Pass 1. """

        # Read the first line and search for 'START'
        first = next(self.contents)
        first_line = SourceLine.parse(first, line_number=1)
        if first_line.mnemonic is not None:
            # If the opcode is 'START', set the locctr to the starting address
            if first_line.mnemonic == 'START':
                self.start_address = int(first_line.operand, 16)
                self.locctr = int(first_line.operand, 16)
                self.program_name = first_line.label

        # Loop through every line excluding the first
        for line_number, line in enumerate(self.contents):
            if not blank_line(line) and not comment(line):
                source_line = SourceLine.parse(line, line_number)
                source_line.location = self.locctr

                # If there is a label, search for it, and/or add it to symtab
                if source_line.label is not None:
                    if source_line.label not in self.symtab:
                        self.symtab[source_line.label] = hex(int(self.locctr))
                    else:
                        raise DuplicateSymbolError(
                                message="A duplicate symbol was found on line: " +
                                str(line_number+2), code=1,
                                line_number=line_number+2, contents=line)

                mnemonic = base_mnemonic(source_line.mnemonic)
                # Search optab for the mnemonic
                if mnemonic in op_table:
                    self.locctr += determine_format(source_line.mnemonic)
                elif mnemonic == 'WORD':
                    self.locctr += 3
                elif mnemonic == 'RESW':
                    self.locctr += 3 * int(source_line.operand)
                elif mnemonic == 'RESB':
                    self.locctr += int(source_line.operand)
                elif mnemonic == 'BYTE':
                    if source_line.operand.startswith('X'):
                        value = source_line.operand.replace("X", '')
                        stripped_value = value.replace("'", '')
                        hex_value = int(stripped_value, 16)
                        self.locctr += (len(hex(hex_value)) - 2) / 2
                    elif source_line.operand.startswith("C"):
                        value = source_line.operand.replace("C", '')
                        stripped_value = value.replace("'", '')
                        self.locctr += len(stripped_value)
                    else:
                        raise LineFieldsError(
                                message="Invalid value for BYTE on line: " +
                                str(line_number+2), code=1,
                                line_number=line_number+2, contents=line)
                elif mnemonic == 'END':
                    # Stop reading through the file contents
                    break
                elif mnemonic == 'BASE':
                    # ignore the base mnemonic on the first pass
                    # this will be taken care of on the second pass
                    pass
                else:
                    raise OpcodeLookupError(
                            message='The mnemonic is invalid on line: ' +
                            str(line_number+2), code=1,
                            line_number=line_number+2, contents=line)

                # Add to the temporary array
                self.temp_contents.append(source_line)
 

    def second_pass(self):
        """ Pass 2. """

        object_code = []

        for source_line in self.temp_contents:
            found_opcode = op_table.get(base_mnemonic(source_line.mnemonic))
            if found_opcode:
                # determine the instruction format
                instr_format = determine_format(source_line.mnemonic)
                
                instruction_output = self.generate_instruction(
                                            source_line.location,
                                            instr_format,
                                            source_line) 
                object_code.append((source_line.location, instruction_output))

            else:
                if source_line.mnemonic == 'WORD':
                    hex_value = hex(int(source_line.operand))
                    stripped_value = hex_value.lstrip("0x")
                    padded_value = stripped_value.zfill(6)
                    object_info = (source_line.mnemonic, source_line.operand,
                                   padded_value)
                    object_code.append((source_line.location, object_info))
                elif source_line.mnemonic == 'BYTE':
                    if source_line.operand.startswith('X'):
                        value = source_line.operand.replace("X", '')
                        stripped_value = value.replace("'", '')
                        object_info = (source_line.mnemonic,
                                       source_line.operand, stripped_value)
                        object_code.append((source_line.location,
                                            object_info))
                    elif source_line.operand.startswith("C"):
                        value = source_line.operand.replace("C", '')
                        stripped_value = value.replace("'", '').encode()
                        hex_value = codecs.encode(stripped_value, "hex")
                        object_info = (source_line.mnemonic,
                                       source_line.operand, hex_value)
                        object_code.append((source_line.location,
                                            object_info))
                elif source_line.mnemonic == 'BASE':
                    self.base = self.symtab.get(source_line.operand)
                elif source_line.mnemonic == 'NOBASE':
                    self.base = None

        self.__generated_objects = object_code

    def generate_instruction(self, line_number, instr_format, source_line):
        if instr_format is 1:
            instruction = Format1(mnemonic=source_line.mnemonic)
        elif instr_format is 2:
            expected_operands = op_table[source_line.mnemonic].operands
            if len(expected_operands) == 2:
                r1, r2 = source_line.operand.split(',')
            elif len(expected_operands) == 1:
                r1, r2 = source_line.operand, None
            instruction = Format2(mnemonic=source_line.mnemonic,
                                  r1=r1, r2=r2)
        elif instr_format is 3:
            instruction = Format3(base=self.base, symtab=self.symtab,
                                  source_line=source_line)
        elif instr_format is 4:
            instruction = Format4(symtab=self.symtab, source_line=source_line)

        return instruction

    def generate_records(self):
        if len(self.__generated_records) > 0:
            return self.generated_records
        last_line = self.generated_objects[len(self.generated_objects)-1]
        if isinstance(last_line[1], Format):
            self.program_length = self.locctr + len(last_line[1].generate()) - \
                    self.start_address
        else:
            self.program_length = self.locctr + len(last_line[1])/2 - \
                    self.start_address

        self.__generated_records = generate_records(
                                   generated_objects=self.generated_objects,
                                   program_name=self.program_name,
                                   start_address=self.start_address,
                                   program_length=self.program_length)
        return self.generated_records

    @property
    def generated_objects(self):
        return self.__generated_objects

    @property
    def generated_records(self):
        return self.__generated_records


def base_mnemonic(mnemonic):
    """ 
    Strips off extra information attached to a mnemonic and returns
    a simple mnemonic.
    """
    if extended(mnemonic):
        return mnemonic[1:]
    else:
        return mnemonic


def determine_format(mnemonic):
    """ Determine the instruction format. """
    if extended(mnemonic):
        return op_table[mnemonic[1:]].format + 1
    else:
        return op_table[mnemonic].format
