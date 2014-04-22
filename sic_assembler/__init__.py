import argparse
import sys

from sic_assembler.assembler import Assembler
from sic_assembler.errors import OpcodeLookupError


def main():
    parser = argparse.ArgumentParser(description='A 2 pass SIC/XE assembler.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser.add_argument("file", help="file to be assembled.")
        parser.add_argument('-o','--outfile', help='output file',
                            default=None, required=False)
        parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                            default=0, help='increase output verbosity')
        args = parser.parse_args()

        try:
            with open(args.file, 'r') as f:
                a = Assembler(f, args.verbosity)
                output_records = a.assemble()
        except IOError:
            print("[IO Error]: The source file could not be opened.")
        except OpcodeLookupError as e:
            print("[OpcodeLookupError] information:")
            print(e.details)
            raise
        else:
            try:
                if args.outfile is None:
                    for record in output_records:
                        print(record)
                else:
                    with open(args.outfile, 'w') as w:
                        for record in output_records:
                            w.write(record)
                            w.write('\n')
            except IOError:
                print("[IO Error]: The output file could not be opened.")
    else:
        a = Assembler(sys.stdin)
        try:
            output_records = a.assemble()
        except StopIteration:
            print("[IO Error]: The source program could not be read from stdin")
        else:
            for record in output_records:
                print(record)


if __name__ == '__main__':
    main()
