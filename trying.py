import os,sys
import re
import pandas as pd
import pathlib

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo', help='foo help')
args = parser.parse_args()
print(args)

