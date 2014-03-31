from collections import namedtuple

# Important Bookmarks:
# Page 50: Assembler Algorithm and Data Structures
# Page 8/9 and 498: Instruction Formats
# Page 496: Instructions

# Represent an instruction
Instr = namedtuple('Instr', 'opcode format')

# Operation code table
op_table = { 'ADD': Instr(0x18, 3),
             'ADDF': Instr(0x58, 3),
             'ADDR': Instr(0x90, 2),
             'AND': Instr(0x40, 3),
             'CLEAR': Instr(0xB4, 2),
             'COMP': Instr(0x28, 3),
             'COMPF': Instr(0x88, 3),
             'COMPR': Instr(0xA0, 2),
             'DIV': Instr(0x24, 3),
             'DIVF': Instr(0x64, 3),
             'DIVR': Instr(0x9C, 2),
             'FIX': Instr(0xC4, 1),
             'FLOAT': Instr(0xC0, 1),
             'HIO': Instr(0xF4, 1),
             'J': Instr(0x3C, 3),
             'JEQ': Instr(0x30, 3),
             'JGT': Instr(0x34, 3),
             'JLT': Instr(0x38, 3),
             'JSUB': Instr(0x48, 3),
             'LDA': Instr(0x00, 3),
             'LDB': Instr(0x68, 3),
             'LDCH': Instr(0x50, 3),
             'LDF': Instr(0x70, 3),
             'LDL': Instr(0x08, 3),
             'LDS': Instr(0x6C, 3),
             'LDT': Instr(0x74, 3),
             'LDX': Instr(0x04, 3),
             'LPS': Instr(0xD0, 3),
             'MULF': Instr(0x60, 3),
             'MULR': Instr(0x98, 2),
             'NORM': Instr(0xC8, 1),
             'OR': Instr(0x44, 3),
             'RD': Instr(0xD8, 3),
             'RMO': Instr(0xAC, 2),
             'RSUB': Instr(0x4C, 3),
             'SHIFTL': Instr(0xA4, 2),
             'SHIFTR': Instr(0xA8, 2),
             'SIO': Instr(0xF0, 1),
             'SSK': Instr(0xEC, 3),
             'STA': Instr(0x0C, 3),
             'STB': Instr(0x78, 3),
             'STCH': Instr(0x54, 3),
             'STF': Instr(0x80, 3),
             'STI': Instr(0xD4, 3),
             'STL': Instr(0x14, 3),
             'STS': Instr(0x7C, 3),
             'STSW': Instr(0xE8, 3),
             'STT': Instr(0x84, 3),
             'STX': Instr(0x10, 3),
             'SUB': Instr(0x1C, 3),
             'SUBF': Instr(0x5C, 3),
             'SUBR': Instr(0x94, 2),
             'SVC': Instr(0xB0, 2),
             'TD': Instr(0xE0, 3),
             'TIO': Instr(0xF8, 1),
             'TIX': Instr(0x2C, 3),
             'TIXR': Instr(0xB8, 2),
             'WD': Instr(0xDC, 3)
           }


# Flags table
flag_table = { 'n': 0b100000,
               'i': 0b010000,
               'x': 0b001000,
               'b': 0b000100,
               'p': 0b000010,
               'e': 0b000001
             }
