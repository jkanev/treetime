from .treetime import *
import sys

def main(args=None):
    """The main routine."""
    
    if args is None:
        args = sys.argv[1:]
    if not len(args):
        TreeTime()
    else:
        TreeTime(filename=args[0])

if __name__ == "__main__":
    main()
