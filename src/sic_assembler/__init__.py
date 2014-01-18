import argparse
import sys

from assembler import assemble


def main():
    parser = argparse.ArgumentParser(description='A 2 pass SIC/XE assembler.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Take action depending on whether or not this is being pipelined
    if sys.stdin.isatty():
        parser.add_argument("file", help="file to be assembled.")
        parser.add_argument('-o','--outfile', help='output file',
                            default='a.out', required=False)
        parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                            default=0, help="increase output verbosity")
        args = parser.parse_args()

        with open(args.file) as f:
            assemble(f, args.verbosity)
    else:
        try:
            import cStringIO as StringIO
        except ImportError:
            import StringIO

        assemble(sys.stdin)
