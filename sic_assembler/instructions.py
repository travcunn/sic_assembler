# Important Bookmarks:
# Page 50: Assembler Algorithm and Data Structures
# Page 8/9 and 498: Instruction Formats
# Page 496: Instructions

class Instr(object):
    """ Represents a single instruction. """
    def __init__(self, opcode, format, operands):
        self.opcode = opcode
        self.format = format
        self.operands = operands


# Operation code table, found on page 496
op_table = { 'ADD':     Instr(0x18, 3, ('m')),
             'ADDF':    Instr(0x58, 3, ('m')),
             'ADDR':    Instr(0x90, 2, ('r1', 'r2')),
             'AND':     Instr(0x40, 3, ('m')),
             'CLEAR':   Instr(0xB4, 2, ('r1')),
             'COMP':    Instr(0x28, 3, ('m')),
             'COMPF':   Instr(0x88, 3, ('m')),
             'COMPR':   Instr(0xA0, 2, ('r1', 'r2')),
             'DIV':     Instr(0x24, 3, ('m')),
             'DIVF':    Instr(0x64, 3, ('m')),
             'DIVR':    Instr(0x9C, 2, ('r1', 'r2')),
             'FIX':     Instr(0xC4, 1, None),
             'FLOAT':   Instr(0xC0, 1, None),
             'HIO':     Instr(0xF4, 1, None),
             'J':       Instr(0x3C, 3, ('m')),
             'JEQ':     Instr(0x30, 3, ('m')),
             'JGT':     Instr(0x34, 3, ('m')),
             'JLT':     Instr(0x38, 3, ('m')),
             'JSUB':    Instr(0x48, 3, ('m')),
             'LDA':     Instr(0x00, 3, ('m')),
             'LDB':     Instr(0x68, 3, ('m')),
             'LDCH':    Instr(0x50, 3, ('m')),
             'LDF':     Instr(0x70, 3, ('m')),
             'LDL':     Instr(0x08, 3, ('m')),
             'LDS':     Instr(0x6C, 3, ('m')),
             'LDT':     Instr(0x74, 3, ('m')),
             'LDX':     Instr(0x04, 3, ('m')),
             'LPS':     Instr(0xD0, 3, ('m')),
             'MULF':    Instr(0x60, 3, ('m')),
             'MULR':    Instr(0x98, 2, ('r1', 'r2')),
             'NORM':    Instr(0xC8, 1, None),
             'OR':      Instr(0x44, 3, ('m')),
             'RD':      Instr(0xD8, 3, ('m')),
             'RMO':     Instr(0xAC, 2, ('r1', 'r2')),
             'RSUB':    Instr(0x4C, 3, None),
             'SHIFTL':  Instr(0xA4, 2, ('r1', 'n')),
             'SHIFTR':  Instr(0xA8, 2, ('r1', 'n')),
             'SIO':     Instr(0xF0, 1, None),
             'SSK':     Instr(0xEC, 3, ('m')),
             'STA':     Instr(0x0C, 3, ('m')),
             'STB':     Instr(0x78, 3, ('m')),
             'STCH':    Instr(0x54, 3, ('m')),
             'STF':     Instr(0x80, 3, ('m')),
             'STI':     Instr(0xD4, 3, ('m')),
             'STL':     Instr(0x14, 3, ('m')),
             'STS':     Instr(0x7C, 3, ('m')),
             'STSW':    Instr(0xE8, 3, ('m')),
             'STT':     Instr(0x84, 3, ('m')),
             'STX':     Instr(0x10, 3, ('m')),
             'SUB':     Instr(0x1C, 3, ('m')),
             'SUBF':    Instr(0x5C, 3, ('m')),
             'SUBR':    Instr(0x94, 2, ('r1', 'r2')),
             'SVC':     Instr(0xB0, 2, ('n')),
             'TD':      Instr(0xE0, 3, ('m')),
             'TIO':     Instr(0xF8, 1, None),
             'TIX':     Instr(0x2C, 3, ('m')),
             'TIXR':    Instr(0xB8, 2, ('r1')),
             'WD':      Instr(0xDC, 3, ('m'))
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
