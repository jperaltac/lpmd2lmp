#!/usr/bin/env python3
"""A Python3 implementation of PSO using MPI4PY Library
   """
#System libs
import sys
import numpy as np

#Local libs
from lmp_cell import ReadDataLPMD
from arguments import passingargs, checkargs

ARGS = passingargs()
ACHK = checkargs(ARGS)

if ACHK != 0:
    print("Error in arguments")
    sys.exit(1)

from_file = ReadDataLPMD(ARGS.file)
N = int(from_file[1])
region = str(from_file[-1][0])
atm_lst = from_file[-2][0]

to_file = "units           metal\n"
to_file += "atom_style      charge\n"
to_file += region+"\n"

for i in range(N):
    to_file += str(atm_lst[i]) + "\n"

ofile = open(str(ARGS.out), 'w')
ofile.write(to_file)

