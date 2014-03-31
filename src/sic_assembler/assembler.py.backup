from errors import LineFieldsError, OpcodeLookupError
from instructions import flag_table, op_table


__all__ = ['assemble']


def assemble(inputfile, verbosity=0):
    """ Assemble the contents of a file-like object. """
    contents = (line.rstrip('\n') for line in inputfile.readlines())

    # Symbol table
    symtab = {}

    for line_number, line in enumerate(contents):
        current_line = line_number + 1
        fields = line.split()
        if len(fields) is 3:
            label = fields[0]
            opcode = fields[1]
            operands = fields[2]
        elif len(fields) is 2:
            opcode = fields[0]
            operands = fields[1]
        elif len(fields) is 1:
            opcode = fields[0]
        else:
            raise LineFieldsError(message='Invalid amount of fields on line ' +
                                  str(current_line), code=1,
                                  line_number=current_line, contents=line)

        try:
            print hex(op_table[opcode].opcode)
        except KeyError:
            raise OpcodeLookupError(message='Invalid opcode mnemonic on line ' +
                                    str(current_line), code=1,
                                    line_number=current_line, contents=line)
