import argparse
import sys

from assembler import Assembler
from errors import OpcodeLookupError


def main():
    parser = argparse.ArgumentParser(description='A 2 pass SIC/XE assembler.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser.add_argument("file", help="file to be assembled.")
        parser.add_argument('-o','--outfile', help='output file',
                            default='a.out', required=False)
        parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                            default=0, help='increase output verbosity')
        parser.add_argument('-l', '--logfile', help='info and error log file',
                            required=False)
        args = parser.parse_args()

        try:
            with open(args.file) as f:
                a = Assembler(f, args.verbosity)
                a.assemble()
        except IOError:
            print("[IO Error]: The file could not be opened.")
        except OpcodeLookupError, e:
            print "[OpcodeLookupError] information:"
            print e.details
            raise
    else:
        a = Assembler(sys.stdin)
        a.assemble()


if __name__ == '__main__':
    main()
