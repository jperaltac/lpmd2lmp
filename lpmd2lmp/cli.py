#!/usr/bin/env python3
"""A Python3 implementation of PSO using MPI4PY Library
   """
#System libs
import sys
import numpy as np

#Local libs
from .lmp_cell import ReadDataLPMD
from .arguments import passingargs, checkargs

def main():
    args = passingargs()
    achk = checkargs(args)

    if achk != 0:
        print("Error in arguments")
        sys.exit(1)

    from_file = ReadDataLPMD(args.file)
    n = int(from_file[1])
    region = str(from_file[-1][0])
    atm_lst = from_file[-2][0]

    all_atoms_string = ''
    cell_string = ''

    # Assignate
    cell_string += region + "\n"
    for i in range(n):
        all_atoms_string += "create_atoms " + str(atm_lst[i]) + "\n"

    to_file = ''

    if args.template:
        template_file = open(args.template, 'r').read()
        to_file = template_file
        to_file = to_file.replace('ALL_ATOM_STRING', all_atoms_string)
        to_file = to_file.replace('CELL_STRING', cell_string)
    else:
        to_file = "units           metal\n"
        to_file += "atom_style      charge\n"
        to_file += cell_string
        to_file += all_atoms_string

    ofile = open(str(args.out), 'w')
    ofile.write(to_file)


if __name__ == "__main__":
    main()

