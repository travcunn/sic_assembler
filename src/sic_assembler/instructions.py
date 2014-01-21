from collections import namedtuple

# Important Bookmarks:
# Page 50: Assembler Algorithm and Data Structures
# Page 8/9 and 498: Instruction Formats
# Page 496: Instructions

# Represent an instruction
Instr = namedtuple('Instr', 'opcode')

# Operation code table
op_table = { 'ADD': Instr(0x18),
             'ADDF': Instr(0x58),
             'ADDR': Instr(0x90),
             'AND': Instr(0x40),
             'CLEAR': Instr(0xB4),
             'COMP': Instr(0x28),
             'COMPF': Instr(0x88),
             'COMPR': Instr(0xA0),
             'DIV': Instr(0x24),
             'DIVF': Instr(0x64),
             'DIVR': Instr(0x9C),
             'FIX': Instr(0xC4),
             'FLOAT': Instr(0xC0),
             'HIO': Instr(0xF4),
             'J': Instr(0x3C),
             'JEQ': Instr(0x30),
             'JGT': Instr(0x34),
             'JLT': Instr(0x38),
             'JSUB': Instr(0x48),
             'LDA': Instr(0x00),
             'LDB': Instr(0x68),
             'LDCH': Instr(0x50),
             'LDF': Instr(0x70),
             'LDL': Instr(0x08),
             'LDS': Instr(0x6C),
             'LDT': Instr(0x74),
             'LDX': Instr(0x04),
             'LPS': Instr(0xD0),
             'MULF': Instr(0x60),
             'MULR': Instr(0x98),
             'NORM': Instr(0xC8),
             'OR': Instr(0x44),
             'RD': Instr(0xD8),
             'RMO': Instr(0xAC),
             'RSUB': Instr(0x4C),
             'SHIFTL': Instr(0xA4),
             'SHIFTR': Instr(0xA8),
             'SIO': Instr(0xF0),
             'SSK': Instr(0xEC),
             'STA': Instr(0x0C),
             'STB': Instr(0x78),
             'STCH': Instr(0x54),
             'STF': Instr(0x80),
             'STI': Instr(0xD4),
             'STL': Instr(0x14),
             'STS': Instr(0x7C),
             'STSW': Instr(0xE8),
             'STT': Instr(0x84),
             'STX': Instr(0x10),
             'SUB': Instr(0x1C),
             'SUBF': Instr(0x5C),
             'SUBR': Instr(0x94),
             'SVC': Instr(0xB0),
             'TD': Instr(0xE0),
             'TIO': Instr(0xF8),
             'TIX': Instr(0x2C),
             'TIXR': Instr(0xB8),
             'WD': Instr(0xDC)
           }


# Flags table
flag_table = { 'n': 0b100000,
               'i': 0b010000,
               'x': 0b001000,
               'b': 0b000100,
               'p': 0b000010,
               'e': 0b000001
             }

