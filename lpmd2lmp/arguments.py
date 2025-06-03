import argparse
import os
import sys
from .parselpmd2 import LPMD2

def passingargs():
    parser = argparse.ArgumentParser(prog='lpmd2lmp', description='Convert lpmd to lammps (lmp) file.')
    parser.add_argument('-f', '--file', help='Input file with atomic configurations at lpmd format.')
    parser.add_argument('-o', '--out', help='Output file')
    parser.add_argument('-t', '--template', help='A template (lammps) file to use as output')
    args = parser.parse_args()
    return args

def barprogress(count, total, status=''):
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))
    percents = float(100.0 * count / float(total))
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    print('[{0:s}] {1:5.2f}{2:s} ...{3:s}\r'.format(bar, percents, '%', status))
    sys.stdout.flush()

def checkargs(args):
    if not args.file:
        print("Input file in lpmd format is mandatory")
        return 1
    if not args.out:
        print("Output file is mandatory")
        return 1
    return 0
