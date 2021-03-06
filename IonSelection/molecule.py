import numpy as np
from functools import reduce


def bondLength(atom1, atom2):

    return np.sqrt((atom1.x-atom2.x)**2+(atom1.y-atom2.y)**2+(atom1.z-atom2.z)**2)

def angles(atom1, atom2, atom3):

    v_1 = [atom1.x-atom2.x, atom1.y - atom2.y, atom1.z - atom2.z]
    v_2 = [atom3.x - atom2.x, atom3.y - atom2.y, atom3.z - atom2.z]

    v_1mag = np.sqrt(v_1[0] ** 2 + v_1[1] ** 2 + v_1[2] ** 2)
    v_1norm = [v_1[0]/v_1mag, v_1[1]/v_1mag, v_1[2]/v_1mag]

    v_2mag = np.sqrt(v_2[0] ** 2 + v_2[1] ** 2 + v_2[2] ** 2)
    v_2norm = [v_2[0] / v_2mag, v_2[1] / v_2mag, v_2[2] / v_2mag]
    if np.abs(v_1norm[0]*v_2norm[0] + v_1norm[1]*v_2norm[1] + v_1norm[2]*v_2norm[2]) <= 1:

        return np.degrees(np.arccos(v_1norm[0]*v_2norm[0] + v_1norm[1]*v_2norm[1] + v_1norm[2]*v_2norm[2]))

    else:
        return np.degrees(np.arccos(v_1norm[0]*v_2norm[0] + v_1norm[1]*v_2norm[1] + v_1norm[2]*v_2norm[2]))

def isWater(atomH1, atomO, atomH2):
    l1 = bondLength(atomH1, atomO)
    l2 = bondLength(atomH2, atomO)
    theta = angles(atomH1, atomO, atomH2)
    # np.abs(1.043 - l1) <= 0.1 and np.abs(1.043 - l2) <= 0.1 and np.abs(theta-105.5) <= 10:
    return (
        np.abs(1.043 - l1) <= 0.15
        and np.abs(1.043 - l2) <= 0.15
        and np.abs(theta - 105.5) <= 15
    )

def isHydroxide(atomH, atomO):
    l = bondLength(atomH,atomO)
    return (np.abs(0.95-l) < 0.5)

def isClustered(ionX, waterH, clusterLength):

    boolVar = [True]
    for waterPair in waterH:

        if bondLength(ionX, waterPair[0]) <= clusterLength or bondLength(ionX, waterPair[1]) <= clusterLength:
            boolVar.append(True)
        else:
            boolVar.append(False)

    return bool(reduce((lambda x, y: x * y), boolVar))

def isIon(ion):
    return True

def isProton(protonHydrogen):
    ##### Could Need Work #####
    return True


