import unittest

from sic_assembler import assembler, instructions
from sic_assembler.assembler import Assembler, SourceLine
from sic_assembler.instructions import Format
from sic_assembler.instructions import  Format1, Format2, Format3, Format4
from sic_assembler.records import generate_header


class TestFieldTypes(unittest.TestCase):
    """ 
    Test each of the methods for parsing the source program.
    """
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
    """
    Test simple programs and check the generated objects and records.
    """
    def setUp(self):
        # test the object code generation from page 58 in the book
        self.a = Assembler(open('test-programs/page58.asm', 'r'))
        self.a.first_pass()
        self.a.second_pass()

    def test_output_objects(self):
        generated_code = []

        for x in self.a.generated_objects:
            if isinstance(x[1], Format):
                generated_code.append(x[1].generate()[2])
            else:
                generated_code.append(x[1][2])

        expected_code = ['17202D', '69202D', '4B101036', '032026', '290000',
                         '332007', '4B10105D', '3F2FEC', '032010', '0F2016',
                         '010003', '0F200D', '4B10105D', '3E2003', '454f46',
                         'B410', 'B400', 'B440', '75101000', 'E32019',
                         '332FFA', 'DB2013', 'A004', '332008', '57C003',
                         'B850', '3B2FEA', '134000', '4F0000', 'F1', 'B410',
                         '774000', 'E32011', '332FFA', '53C003', 'DF2008',
                         'B850', '3B2FEF', '4F0000', '05']

        self.assertTrue(generated_code == expected_code)

    def test_output_records(self):
        generated_code = []

        for x in self.a.generated_objects:
            if isinstance(x[1], Format):
                generated_code.append((x[0], x[1].generate()[2]))
            else:
                generated_code.append((x[0], x[1][2]))




class TestInstructionGeneration(unittest.TestCase):
    """
    Test instruction generation for each instruction format.
    """
    def test_format_1(self):
        line = "TIO"
        source_line = SourceLine.parse(line, 1)

        instruction = Format1(mnemonic=source_line.mnemonic)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "F8")

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


class TestRecordGeneration(unittest.TestCase):
    def test_header(self):
        print generate_header('COPY', 0, )


if __name__ == '__main__':
    unittest.main()
