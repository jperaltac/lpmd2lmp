#!/usr/bin/env python3


import numpy as np
from parselpmd2 import LPMD2

def py_ang(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'    """
    cosang = np.dot(v1, v2)
    sinang = np.linalg.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def cell_to_lammps(A, B, C):
    """ Convert tree cell vector A, B, and C to LAMMPS format
        From http://lammps.sandia.gov/doc/Section_howto.html#howto-12
        This function take an A=(Ax, Ay, Az), B=(Bx, By, Bz), and C = (Cx, Cy, Cz)
        and convert to a prism input in lammps using xlo xhi, etc."""
    nA, nB, nC = np.linalg.norm(A),  np.linalg.norm(B), np.linalg.norm(C)
    vnA = A/nA
    vAxB = np.cross(A,B)
    vnAxB = vAxB/np.linalg.norm(vAxB)

    #Convert A, B, and C to lammps a, b, and, c
    ax, ay, az = np.linalg.norm(A), 0.0, 0.0
    bx, by, bz = np.inner(B, vnA), np.linalg.norm(np.cross(vnA, B)), 0.0
    cx, cy, cz = np.inner(C, vnA), np.inner(C, np.cross(vnAxB, vnA)), np.linalg.norm(np.inner(C, vnAxB))
    a, b, c = np.array([ax, ay, az]), np.array([bx, by, bz]), np.array([cx, cy, cz])

    #Cell angles in rad
    alpha = py_ang(b, c)
    beta = py_ang(a, c)
    gamma = py_ang(a, b)

    lx = np.linalg.norm(a)
    xy = np.linalg.norm(b)*np.cos(gamma)
    xz = np.linalg.norm(c)*np.cos(beta)
    ly = np.sqrt(np.linalg.norm(b)**2 - xy**2)
    yz = (np.linalg.norm(b)*np.linalg.norm(c)*np.cos(alpha) - xy*xz)/ly
    lz = np.sqrt(np.linalg.norm(c)**2 - xz**2 - yz**2)

    cell = "region box prism {0:.6f} {1:.6f} {2:.6f} {3:.6f} {4:.6f} {5:.6f} {6:.6f} {7:.6f} {8:.6f}".format(0.0,lx,0.0,ly,0.0,lz,xy,xz,yz)
    return cell

def X_to_lammps(A, B, C, X):
    """ Convert X vector in A, B, C to lammps basis (a, b, c)
        This function take an A=(Ax, Ay, Az), B=(Bx, By, Bz), and C = (Cx, Cy, Cz)
        """
    nA, nB, nC = np.linalg.norm(A),  np.linalg.norm(B), np.linalg.norm(C)
    vnA = A/nA
    vAxB = np.cross(A,B)
    vnAxB = vAxB/np.linalg.norm(vAxB)

    #Convert A, B, and C to lammps a, b, and, c
    ax, ay, az = np.linalg.norm(A), 0.0, 0.0
    bx, by, bz = np.inner(B, vnA), np.linalg.norm(np.cross(vnA, B)), 0.0
    cx, cy, cz = np.inner(C, vnA), np.inner(C, np.cross(vnAxB, vnA)), np.linalg.norm(np.inner(C, vnAxB))
    a, b, c = np.array([ax, ay, az]), np.array([bx, by, bz]), np.array([cx, cy, cz])

    M1 = np.column_stack((a, b, c))
    M2 = np.array([np.cross(B,C), np.cross(C,A), np.cross(A,B)])
    V = np.dot(np.cross(A,B),C)
    M3 = np.dot(M1, (1/V)*M2)
    return np.dot(M3, X)

def ReadDataLPMD(filelpmd):
    atoms_lmp, cell_lmp = [], []
    configs = LPMD2()
    try:
        configs.Read(filelpmd)
    except:
        if rnk == 0: print("Cannot open the ", filelpmd, " file.")
        exit(0)
    print("Readed ", len(configs), " configs. Assuming all have the same number of atoms.")
    nconfigs = len(configs)
    natoms   = len(configs[0]) #Assume same number of atoms
    #Count atomic species
    cfg = configs[0]
    symbols = []
    for _i in range(len(cfg)):
        symbols.append(cfg.Tag('SYM', _i))
    all_types = sorted(list(set(symbols)))
    for i in range(len(configs)):
        cfg = configs[i]
        tmp = []
        v1, v2, v3 = cfg.cell[0], cfg.cell[1], cfg.cell[2]
        A = np.array([v1[0], v1[1], v1[2]])
        B = np.array([v2[0], v2[1], v2[2]])
        C = np.array([v3[0], v3[1], v3[2]])
        for j in range(len(cfg)):
            pos = cfg.PackTags(('X', 'Y', 'Z'), j)
            sym = cfg.Tag('SYM', j)
            idx = int(all_types.index(sym)) + 1
            x = pos[0]*v1[0] + pos[1]*v2[0] + pos[2]*v3[0]
            y = pos[0]*v1[1] + pos[1]*v2[1] + pos[2]*v3[1]
            z = pos[0]*v1[2] + pos[1]*v2[2] + pos[2]*v3[2]
            new_pos = X_to_lammps(A, B, C, np.array([x, y, z]))
            tmp.append(str(idx) + " single " + str(new_pos[0]) + " " + str(new_pos[1]) + " " + str(new_pos[2]) + " remap yes ")
        atoms_lmp.append(tmp)
        cell_lmp.append(cell_to_lammps(A, B, C))
        del(tmp); del(cfg)
    del configs
    return (nconfigs, natoms, atoms_lmp, cell_lmp)
