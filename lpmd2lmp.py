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

ALL_ATOMS_STRING = ''
CELL_STRING = ''

#Assignate
CELL_STRING += region+"\n"
for i in range(N):
    ALL_ATOMS_STRING += "create_atoms " + str(atm_lst[i]) + "\n"

to_file = ''

if ARGS.template:
    with open(ARGS.template, 'r') as f:
        template_file = f.read()
    to_file = template_file
    to_file = to_file.replace('ALL_ATOM_STRING', ALL_ATOMS_STRING)
    to_file = to_file.replace('CELL_STRING', CELL_STRING)
else:
    to_file = "units           metal\n"
    to_file += "atom_style      charge\n"
    to_file += CELL_STRING
    to_file += ALL_ATOMS_STRINGS

with open(str(ARGS.out), 'w') as ofile:
    ofile.write(to_file)

