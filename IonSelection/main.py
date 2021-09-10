import re
import pandas as pd
import atom as atom
import cluster as cl
import argparse
import math


########## COMMANDLINE ARGUMENT PASSING #########

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", action="store", help="CP2K trajectory file")
parser.add_argument("-r", "--radius", action="store", help="g(r) for cluster criteria in Angstroms")
parser.add_argument("-i", "--ion", action="store", help="Ion in water cluster, write as: Cl, Br, OH, ect.")
parser.add_argument("-A", "--age", action="store", help="Age trajectory, i.e. t0=t/2, tn=t [Y],[N]")
args = parser.parse_args()
clusterLength = float(args.radius)
ion = str(args.ion)
cp2k = args.file
age = args.age

##### If the ion a halide then add this to the pattern search cp2k trajectory ######

if ion == "OH" or ion == "H":
    cp2K_search = "(?:i |H|O)"
else:
    cp2K_search = "(?:i |H|O)"
    cp2K_search = cp2K_search + ion
    cp2K_search = cp2K_search + ")"

#### Send pattern to data read in in atom.py and return them as a pandas dataframe###
pattern = re.compile(cp2K_search)
dataFrameList = atom.dataIn(cp2k, pattern)
maxFrame = dataFrameList[1]
clusterSize = dataFrameList[2]
pdFrames = pd.DataFrame.from_records([Frame.to_dict() for Frame in dataFrameList[0]])
itr = 1

age = math.floor(maxFrame/2) if age == "Y" else 0
##### find if ion is hydroxide #####
if ion == "OH":
    for cluster in range(age, maxFrame):
        pdFrame_0 = pdFrames.loc[cluster:((clusterSize - 1) + cluster), :]
        #### Get cluster infromation for specific data frame #####
        clusterMe = cl.clusterHydroxide(pdFrame_0, clusterSize, clusterLength)
        clusterBool = clusterMe[0]
        waterHydrogen = clusterMe[1]
        waterOxygen = clusterMe[2]
        hydroxideOxygen = clusterMe[3]
        hydroxideHydrogen = clusterMe[4]

        if clusterBool:
            ## If it is a cluster print the configurations ##
            cl.printClusterHydroxide(waterHydrogen, waterOxygen, hydroxideOxygen, hydroxideHydrogen, cluster, itr)
            itr += 1
elif ion == "H":
    for cluster in range(age, maxFrame):
        pdFrame_0 = pdFrames.loc[cluster:((clusterSize - 1) + cluster), :]
        clusterMe = cl.clusterProton(pdFrame_0, clusterSize, clusterLength)
        clusterBool = clusterMe[0]
        waterHydrogen = clusterMe[1]
        waterOxygen = clusterMe[2]
        protonHydrogen = clusterMe[3]

        if clusterBool:
            cl.printClusterHydroxide(waterHydrogen, waterOxygen, protonHydrogen, cluster, itr)
            itr += 1

elif ion in {"F", "Cl", "Br", "I"}:
    print("Hello")
    for cluster in range(age, maxFrame):
        pdFrame_0 = pdFrames.loc[cluster:((clusterSize - 1) + cluster), :]
        clusterMe = cl.clusterIon(pdFrame_0, clusterSize, clusterLength, ion)
        clusterBool = clusterMe[0]
        waterHydrogen = clusterMe[1]
        waterOxygen = clusterMe[2]
        ionFrame = clusterMe[3]

        if clusterBool:
            cl.printClusterIon(waterHydrogen, waterOxygen, ionFrame, cluster, itr)
            itr += 1

else:
    print("Ion not available")


print("Number of time steps: " + str(maxFrame - age))
print("Number of time steps clustered: " + str(itr - 1))
print("\n\n")
print("Naive p(n) = " + str(float((itr - 1)/(maxFrame - age))))
