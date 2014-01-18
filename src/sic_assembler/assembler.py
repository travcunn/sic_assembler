from instructions import flag_table, op_table


__all__ = ['assemble']


def contains_label(line):
    """ Returns whether or not a line contains a label. """
    return line[0].isalpha()


def assemble(inputfile, verbosity=0):
    """ Assemble the contents of a file-like object. """
    contents = (line.rstrip('\n') for line in inputfile.readlines())
    for line in contents:
        fields = line.split()
        if contains_label(line):
            if len(fields) is 3:
                print hex(op_table[fields[1]].opcode)
        else:
            print hex(op_table[fields[0]].opcode)



