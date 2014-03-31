import unittest

from sic_assembler import assembler


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
        self.assertTrue(assembler.indexed(indexed_operand))
        invalid_syntax = "BUFFER, X"
        self.assertFalse(assembler.indexed(invalid_syntax))

    def test_indirect_addressing(self):
        indirect_operand = "@RETADR"
        self.assertTrue(assembler.indirect(indirect_operand))
        non_indirect_operand = "RETADR"
        self.assertFalse(assembler.indirect(non_indirect_operand))

    def test_immediate_operand(self):
        operand = "#3355"
        self.assertTrue(assembler.immediate(operand))
        non_immediate = "ZERO"
        self.assertFalse(assembler.immediate(non_immediate))

    def test_extended(self):
        opcode = "+LDT"
        self.assertTrue(assembler.extended(opcode))
        non_extended = "LDT"
        self.assertFalse(assembler.extended(non_extended))

    def test_literal(self):
        literal = "=X'05'"
        self.assertTrue(assembler.literal(literal))
        non_literal = "X"
        self.assertFalse(assembler.literal(non_literal))


class TestSimpleAssemblyFile(unittest.TestCase):
    def test_simple_assembly(self):
        # test the object code generation from page 47 in the book
        test_file = file('test-programs/simple-program.asm')
        a = assembler.Assembler(test_file)
        a.assemble()

        for x in a.generated_objects:
            print x


if __name__ == '__main__':
    unittest.main()
