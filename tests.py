import unittest

from sic_assembler import assembler
from sic_assembler import instructions
from sic_assembler.assembler import Assembler, SourceLine
from sic_assembler.instructions import Format2, Format3, Format4


class TestFieldTypes(unittest.TestCase):
    def test_comment(self):
        comment_line = ".     SUBROUTINE TO WRITE RECORD FROM BUFFER"
        self.assertTrue(assembler.comment(comment_line))
        non_comment_line = "WLOOP    CLEAR     X"
        self.assertFalse(assembler.comment(non_comment_line))

    def test_blank_line(self):
        blank_line = "         "
        self.assertTrue(assembler.blank_line(blank_line))
        non_blank_line = "COPY      START      0"
        self.assertFalse(assembler.blank_line(non_blank_line))

    def test_indexed_addressing(self):
        indexed_operand = "BUFFER,X"
        self.assertTrue(instructions.indexed(indexed_operand))
        invalid_syntax = "BUFFER, X"
        self.assertFalse(instructions.indexed(invalid_syntax))

    def test_indirect_addressing(self):
        indirect_operand = "@RETADR"
        self.assertTrue(instructions.indirect(indirect_operand))
        non_indirect_operand = "RETADR"
        self.assertFalse(instructions.indirect(non_indirect_operand))

    def test_immediate_operand(self):
        operand = "#3355"
        self.assertTrue(instructions.immediate(operand))
        non_immediate = "ZERO"
        self.assertFalse(instructions.immediate(non_immediate))

    def test_extended(self):
        opcode = "+LDT"
        self.assertTrue(instructions.extended(opcode))
        non_extended = "LDT"
        self.assertFalse(instructions.extended(non_extended))

    def test_literal(self):
        literal = "=X'05'"
        self.assertTrue(instructions.literal(literal))
        non_literal = "X"
        self.assertFalse(instructions.literal(non_literal))


class TestSimpleAssemblyFile(unittest.TestCase):
    def test_simple_assembly(self):
        # test the object code generation from page 58 in the book
        test_file = file('test-programs/page58.asm')
        a = Assembler(test_file)

        # lets step through each pass separately
        a.first_pass()

        a.second_pass()

        expected_objects = [('STL', '0x30', '17202D'),
                            ('LDB', '0x33', '69202D'),
                            ('JSUB', '0x1036', '4B101036'),
                            ('LDA', '0x33', '032026'),
                            ('COMP', '0', '290000'),
                            ('JEQ', '0x1a', '332007'),
                            ('JSUB', '0x105d', '4B10105D'),
                            ('J', '0x6', '3F2FEC'),
                            ('LDA', '0x2d', '032010'),
                            ('STA', '0x36', '0F2016'),
                            ('LDA', '3', '010003'),
                            ('STA', '0x33', '0F200D'),
                            ('JSUB', '0x105d', '4B10105D'),
                            ('J', '0x30', '3E2003'),
                            ('BYTE', "C'EOF'", '454f46'),
                            ('CLEAR', ('X', None), 'B410'),
                            ('CLEAR', ('A', None), 'B400'),
                            ('CLEAR', ('S', None), 'B440'),
                            ('LDT', '1000', '75101000'),
                            ('TD', '0x105c', 'E32019'),
                            ('JEQ', '0x1040', '332FFA'),
                            ('RD', '0x105c', 'DB2013'),
                            ('COMPR', ('A', 'S'), 'A004'),
                            ('JEQ', '0x1056', '332008'),
                            ('STCH', '0x36', '57C003'),
                            ('TIXR', ('T', None), 'B850'),
                            ('JLT', '0x1040', '3B2FEA'),
                            ('STX', '0x33', '134000'),
                            ('RSUB', 0, '4F0000'),
                            ('BYTE', "X'F1'", 'F1'),
                            ('CLEAR', ('X', None), 'B410'),
                            ('LDT', '0x33', '774000'),
                            ('TD', '0x1076', 'E32011'),
                            ('JEQ', '0x1062', '332FFA'),
                            ('LDCH', '0x36', '53C003'),
                            ('WD', '0x1076', 'DF2008'),
                            ('TIXR', ('T', None), 'B850'),
                            ('JLT', '0x1062', '3B2FEF'),
                            ('RSUB', 0, '4F0000'),
                            ('BYTE', "X'05'", '05')]

        self.assertTrue(a.generated_objects == expected_objects)


class TestInstructionGeneration(unittest.TestCase):
    def test_format_2_one_register(self):
        line = "TIXR    T"
        source_line = SourceLine.parse(line, 1)

        instruction = Format2(mnemonic=source_line.mnemonic,
                              r1=source_line.operand, r2=None)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "B850")

    def test_format_2_two_registers(self):
        line = "COMPR   A,S"
        source_line = SourceLine.parse(line, 1)

        r1, r2 = source_line.operand.split(',')
        instruction = Format2(mnemonic=source_line.mnemonic,
                              r1=r1, r2=r2)

        results = instruction.generate()

        self.assertTrue(results[2] == "A004")

    def test_format_3_simple(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['RETADR'] = '30'

        line = "FIRST   STL     RETADR"
        source_line = SourceLine.parse(line, 1)
        source_line.location = int('0000', 16)

        instruction = Format3(base=None, symtab=symtab,
                              source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "17202D")

    def test_format_3_immediate(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['LENGTH'] = '33'

        line = "LDB     #LENGTH"
        source_line = SourceLine.parse(line, 2)
        source_line.location = int('0003', 16)

        instruction = Format3(base=None, symtab=symtab,
                              source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "69202D")
    
    def test_format_3_base_relative_with_indexing(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['BUFFER'] = '36'

        line = "STCH    BUFFER,X"
        source_line = SourceLine.parse(line, 1)
        source_line.location = int('104E', 16)

        base = hex(51)

        instruction = Format3(base=base, symtab=symtab,
                              source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "57C003")

    def test_format_4_simple(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['RDREC'] = '1036'

        line = "+JSUB   RDREC"
        source_line = SourceLine.parse(line, 4)
        source_line.location = int('0006', 16)

        instruction = Format4(symtab=symtab, source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "4B101036")

    def test_format_4_immediate_value(self):
        symtab = dict()

        line = "+LDT   #4096"
        source_line = SourceLine.parse(line, 1)
        source_line.location = int('103C', 16)

        instruction = Format4(symtab=symtab, source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "75101000")

    def test_format_4_immediate_lookup_value(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['MAXLEN'] = '1000'

        line = "+LDT   #MAXLEN"
        source_line = SourceLine.parse(line, 1)
        source_line.location = int('103C', 16)

        instruction = Format4(symtab=symtab, source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "75101000")




if __name__ == '__main__':
    unittest.main()
