import unittest

from sic_assembler import assembler
from sic_assembler import instructions
from sic_assembler.assembler import Assembler, SourceLine
from sic_assembler.instructions import Format3


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
        # test the object code generation from page 47 in the book
        test_file = file('test-programs/page58.asm')
        a = Assembler(test_file)

        # lets step through each pass separately
        a.first_pass()

        a.second_pass()

        for x in a.generated_objects:
            print x


class TestInstructionGeneration(unittest.TestCase):
    def test_format_3_simple(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['RETADR'] = hex(48)

        line = "FIRST   STL     RETADR"
        source_line = SourceLine.parse(line, 1)
        source_line.location = 0

        instruction = Format3(base=None, symtab=symtab,
                              source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "17202D")

    def test_format_3_immediate(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['LENGTH'] = hex(51)

        line = "LDB     #LENGTH"
        source_line = SourceLine.parse(line, 2)
        source_line.location = 3

        instruction = Format3(base=None, symtab=symtab,
                              source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "69202D")
    
    def test_base_relative_with_indexing(self):
        symtab = dict()

        # add a symbol to the symbol table for lookup
        symtab['BUFFER'] = hex(54)

        line = "STCH    BUFFER,X"
        source_line = SourceLine.parse(line, 1)
        source_line.location = int('104E', 16)

        base = hex(51)

        instruction = Format3(base=base, symtab=symtab,
                              source_line=source_line)
        
        results = instruction.generate()

        self.assertTrue(results[2] == "57C003")



if __name__ == '__main__':
    unittest.main()
