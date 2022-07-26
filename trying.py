import os,sys
import pathlib

import argparse
parser = argparse.ArgumentParser(prog= __file__, description='Process some integers.')

parser.add_argument("--verbosity", help="increase output verbosity")
args = parser.parse_args()
print(args)

if args.verbosity:
    print(args.verbosity)
else:
    print(args.verbosity)

