# lpmd2lmp

`lpmd2lmp` converts configuration files produced by [LPMD](https://github.com/la-villa/lpmd/) into a simple LAMMPS input script. The resulting file contains the simulation cell definition and commands to create each atom.

## Requirements

* Python 3
* [NumPy](https://numpy.org/) library

Install the dependency with `pip` if it is not already available:

```bash
pip install numpy
```

## Usage

The converter expects the input file in LPMD 2.0 format and the name of the
destination file:

```bash
python lpmd2lmp.py -f Examples/one.lpmd -o one.in
```

This writes a LAMMPS input file `one.in` with a minimal header and the generated
`create_atoms` commands.  If you already have a template LAMMPS script you can
use it with the `-t` option.  The placeholders `CELL_STRING` and
`ALL_ATOM_STRING` inside the template are replaced with the generated region and
atom creation commands:

```bash
python lpmd2lmp.py -f Examples/one.lpmd -o one.in -t my_template.in
```

The `Examples/one.lpmd` file supplied in this repository can be used to test the
converter.
