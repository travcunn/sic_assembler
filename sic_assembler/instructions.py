from sic_assembler.errors import InstructionError, LineFieldsError, UndefinedSymbolError


class Instr(object):
    """ Represents a single instruction. """
    def __init__(self, opcode, format, operands):
        self.__opcode = opcode
        self.__format = format
        self.__operands = operands

    @property
    def opcode(self):
        return self.__opcode

    @property
    def format(self):
        return self.__format

    @property
    def operands(self):
        return self.__operands


# Operation code table, found on page 496
op_table = { 'ADD':     Instr('18', 3, ['m']),
             'ADDF':    Instr('58', 3, ['m']),
             'ADDR':    Instr('90', 2, ['r1', 'r2']),
             'AND':     Instr('40', 3, ['m']),
             'CLEAR':   Instr('B4', 2, ['r1']),
             'COMP':    Instr('28', 3, ['m']),
             'COMPF':   Instr('88', 3, ['m']),
             'COMPR':   Instr('A0', 2, ['r1', 'r2']),
             'DIV':     Instr('24', 3, ['m']),
             'DIVF':    Instr('64', 3, ['m']),
             'DIVR':    Instr('9C', 2, ['r1', 'r2']),
             'FIX':     Instr('C4', 1, None),
             'FLOAT':   Instr('C0', 1, None),
             'HIO':     Instr('F4', 1, None),
             'J':       Instr('3C', 3, ['m']),
             'JEQ':     Instr('30', 3, ['m']),
             'JGT':     Instr('34', 3, ['m']),
             'JLT':     Instr('38', 3, ['m']),
             'JSUB':    Instr('48', 3, ['m']),
             'LDA':     Instr('00', 3, ['m']),
             'LDB':     Instr('68', 3, ['m']),
             'LDCH':    Instr('50', 3, ['m']),
             'LDF':     Instr('70', 3, ['m']),
             'LDL':     Instr('08', 3, ['m']),
             'LDS':     Instr('6C', 3, ['m']),
             'LDT':     Instr('74', 3, ['m']),
             'LDX':     Instr('04', 3, ['m']),
             'LPS':     Instr('D0', 3, ['m']),
             'MULF':    Instr('60', 3, ['m']),
             'MULR':    Instr('98', 2, ['r1', 'r2']),
             'NORM':    Instr('C8', 1, None),
             'OR':      Instr('44', 3, ['m']),
             'RD':      Instr('D8', 3, ['m']),
             'RMO':     Instr('AC', 2, ['r1', 'r2']),
             'RSUB':    Instr('4C', 3, None),
             'SHIFTL':  Instr('A4', 2, ['r1', 'n']),
             'SHIFTR':  Instr('A8', 2, ['r1', 'n']),
             'SIO':     Instr('F0', 1, None),
             'SSK':     Instr('EC', 3, ['m']),
             'STA':     Instr('0C', 3, ['m']),
             'STB':     Instr('78', 3, ['m']),
             'STCH':    Instr('54', 3, ['m']),
             'STF':     Instr('80', 3, ['m']),
             'STI':     Instr('D4', 3, ['m']),
             'STL':     Instr('14', 3, ['m']),
             'STS':     Instr('7C', 3, ['m']),
             'STSW':    Instr('E8', 3, ['m']),
             'STT':     Instr('84', 3, ['m']),
             'STX':     Instr('10', 3, ['m']),
             'SUB':     Instr('1C', 3, ['m']),
             'SUBF':    Instr('5C', 3, ['m']),
             'SUBR':    Instr('94', 2, ['r1', 'r2']),
             'SVC':     Instr('B0', 2, ['n']),
             'TD':      Instr('E0', 3, ['m']),
             'TIO':     Instr('F8', 1, None),
             'TIX':     Instr('2C', 3, ['m']),
             'TIXR':    Instr('B8', 2, ['r1']),
             'WD':      Instr('DC', 3, ['m'])
           }


flag_table = { 'n': 0b100000,
               'i': 0b010000,
               'x': 0b001000,
               'b': 0b000100,
               'p': 0b000010,
               'e': 0b000001
             }


# page 5 and 7 of the book
registers_table = {'A':  0,
                   'X':  1,
                   'L':  2,
                   'B':  3,
                   'S':  4,
                   'T':  5,
                   'F':  6,
                   'PC': 8,
                   "SW": 9
                  }


# Indexed addressing
indexed = lambda x: str(x).endswith(',X')
# Indirect addressing
indirect = lambda x: str(x).startswith('@')
# An immediate operand
immediate = lambda x: str(x).startswith('#')
# An extended format instruction
extended = lambda x: str(x).startswith('+')
# Literal
literal = lambda x: str(x).startswith('=')


def to_binary(hex_string):
    return bin(int(str(hex_string), 16))[2:]


def twos_complement(value, length):
    if value < 0:
        value = (1 << length) + value
    out_format = '{:0%ib}' % length
    
    return out_format.format(value)


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
    def __init__(self, mnemonic):
        self._mnemonic = mnemonic

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")

        output = ""

        # lookup the opcode
        opcode_lookup = op_table[self._mnemonic].opcode
        output += str(opcode_lookup)

        return self._mnemonic, None, output

    def __repr__(self):
        return "<Format1: mnemonic=%s>" % self._mnemonic


class Format2(Format):
    """ Format 2 instruction class.

         8       4     4
     ======================
    |    op    | r1 |  r2  |
     ======================

    """
    def __init__(self, mnemonic, r1, r2):
        self._mnemonic = mnemonic
        self._r1 = r1
        self._r2 = r2

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")

        output = ""

        # lookup the opcode
        opcode_lookup = op_table[self._mnemonic].opcode
        output += str(opcode_lookup)

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

        return self._mnemonic, (self._r1, self._r2), output

    def __repr__(self):
        return "<Format2: mnemonic=%s r1=%s r2=%s>" % \
                (self._mnemonic, self._r1, self._r2)


class Format3(Format):
    """ Format 3 instruction class.

        6      1   1   1   1   1   1         12
     =================================================
    |   op   | n | i | x | b | p | e |      disp      |
     =================================================

    """
    def __init__(self, base, symtab, source_line):
        self._base = base
        self._symtab = symtab

        self._location = source_line.location
        
        self._mnemonic = source_line.mnemonic
        self._flags, self._n, self._i = determine_flags(source_line)
        self._disp = source_line.operand
        self._line_number = source_line.line_number
        self._contents = source_line

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")

        output = ""

        # op
        opcode_lookup = int(str(op_table[self._mnemonic].opcode), 16)

        if self._n:
            opcode_lookup += 2
        if self._i:
            opcode_lookup += 1
        op = twos_complement(opcode_lookup, 6)

        is_digit = False
        has_operands = False

        if self._disp is not None and not literal(self._disp):
            has_operands = True
            if indexed(self._disp):
                self._disp = self._disp[:len(self._disp)-2]
                symbol_address = self._symtab.get(self._disp)
            elif indirect(self._disp):
                self._disp = self._disp[1:]
                symbol_address = self._symtab.get(self._disp)
            elif immediate(self._disp):
                self._disp = self._disp[1:]
                if str(self._disp).isdigit():
                    symbol_address = self._disp
                    is_digit = True
                else:
                    symbol_address = self._symtab.get(self._disp)
            else:
                symbol_address = self._symtab.get(self._disp)

            if symbol_address is not None:
                self._disp = symbol_address
            else:
                self._disp = 0
                raise UndefinedSymbolError(
                        message='Undefined symbol on line: ' +
                        str(self._line_number+1), code=1,
                        contents=self._contents)
        #TODO: process the literal here in an elif
        else:
            self._disp = 0

        if not is_digit and has_operands:
            # Try PC relative then base relative, or raise an error
            if (-2048 <= self.__pc_relative() <= 2047):
                self._flags += flag_table['p']
                disp = twos_complement(self.__pc_relative(), 12)
            elif(0 <= self.__base_relative() <= 4095):
                self._flags += flag_table['b']
                disp = to_binary(self.__base_relative()).zfill(12)
            else:
                raise InstructionError(
                    message="Neither PC or Base relative addressing could " +
                            "be used."
                )
        else:
            disp = twos_complement(int(self._disp), 12)

        # flags
        flags = to_binary(hex(self._flags))

        # combine each section
        output += op
        output += flags.zfill(4)
        output += disp

        hex_output = hex(int(output, 2))[2:].zfill(6).upper()

        return self._mnemonic, self._disp, hex_output

    def __pc_relative(self):
        """ Calculate the PC relative address. """
        pc = int(str(self._disp), 16) - 3
        disp = int(self._location)
        return pc - disp

    def __base_relative(self):
        """ Calculate the Base relative address. """
        if self._base is None:
            raise InstructionError(message="BASE directive not set")
        base = int(str(self._base), 16)
        disp = int(str(self._disp), 16)

        return disp - base

    def __repr__(self):
        return "<Format3: mnemonic=%s n=%s i=%s flags=%s disp=%s>" % \
                (self._mnemonic, self._n, self._i, self._flags, self._disp)


class Format4(Format):
    """ Format 4 instruction class.

        6      1   1   1   1   1   1              20
     ============================================================
    |   op   | n | i | x | b | p | e |          address          |
     ============================================================
    """
    def __init__(self, symtab, source_line):
        self._symtab = symtab

        self._location = source_line.location
        
        self._mnemonic = source_line.mnemonic[1:]
        self._flags, self._n, self._i = determine_flags(source_line)
        self._disp = source_line.operand
        self._line_number = source_line.line_number
        self._contents = source_line

    def generate(self):
        """ Generate the machine code for the instruction. """
        if self._mnemonic is None:
            raise LineFieldsError(message="A mnemonic was not specified.")

        output = ""

        # op
        opcode_lookup = int(str(op_table[self._mnemonic].opcode), 16)

        if self._n:
            opcode_lookup += 2
        if self._i:
            opcode_lookup += 1
        op = twos_complement(opcode_lookup, 6)

        if self._disp is not None and not literal(self._disp):
            if immediate(self._disp):
                self._disp = self._disp[1:]
                if str(self._disp).isdigit():
                    symbol_address = hex(int(self._disp))[2:]
                else:
                    symbol_address = self._symtab.get(self._disp)
            else:
                symbol_address = self._symtab.get(self._disp)

            if symbol_address is not None:
                self._disp = symbol_address
            else:
                self._disp = 0
                raise UndefinedSymbolError(
                        message='Undefined symbol on line: ' +
                        str(self._line_number+1), code=1,
                        contents=self._contents)
        #TODO: process the literal here in an elif
        else:
            self._disp = 0

        disp = twos_complement(int(self._disp, 16), 20)

        # flags
        flags = to_binary(hex(self._flags))

        # combine each section
        output += op
        output += flags.zfill(4)
        output += disp

        hex_output = hex(int(output, 2))[2:].zfill(6).upper()

        return self._mnemonic, self._disp, hex_output

    def __repr__(self):
        return "<Format3: mnemonic=%s n=%s i=%s flags=%s disp=%s>" % \
                (self._mnemonic, self._n, self._i, self._flags, self._disp)


def determine_flags(source_line):
    """ Calculate the flags given a SourceLine object. """
    
    # initially there are no flags set
    flags = 0
    n = False
    i = False

    if immediate(source_line.operand):
        i = True
    elif indirect(source_line.operand):
        n = True
    else:
        n, i = True, True

    if indexed(source_line.operand):
        if not n and not i:
            raise LineFieldsError(
                    message="Indexed addressing cannot be used with" \
                            "immediate or indirect addressing modes.")
        else:
            flags += flag_table['x']

    if extended(source_line.mnemonic):
        flags += flag_table['e']

    return flags, n, i


def step():
    raw_input(">>")
