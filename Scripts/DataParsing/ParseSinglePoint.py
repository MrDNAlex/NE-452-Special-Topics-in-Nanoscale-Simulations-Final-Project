
# Gameplan
# Do something similar to the GeoOpt Script
# Create same table for the Final Single Point Energy
# Dedicate one column to 5/2RT value (T = 295.15) (convert to hartree)
# Create another 5 columns for the enthalpy values

from ncl.Orca import OrcaOutputFile
from Data import FUNCTIONALS, MOLECULES, ATOMS
import pandas as pd
import os

# Initialize the Data Frame
dataFrame = pd.DataFrame(
    columns=["Atom Name", "LDA Energy", "PBE Energy", "B3LYP Energy", "wB97x-D3 Energy", "M06-2X Energy"]
)

outputFiles = {}

# Find the path to the Single Point Output files
for path, dirs, files in os.walk("Data\\SinglePoint"):

    if len(files) == 0:
        continue
    
    atomName = path.split("\\")[-1]
    outputFiles[atomName] = []

    # Add the files outright because no files are found
    for file in files:
        outputFiles[atomName].append(os.path.join(path, file))

print(outputFiles)

# Write the Data Frame
for atom in ATOMS:
    row = [atom]
    
    for func in FUNCTIONALS:
        # Find the Appropriate file in the proper order, add the Final Single Point Energy to the row
        filePath = next((f for f in outputFiles[atom] if func in f), None)
        row.append(OrcaOutputFile(filePath).getFinalEnergy())
    
    dataFrame.loc[len(dataFrame)] = row
    
print(dataFrame)
dataFrame.to_csv("Results/AtomEnergies.csv", index=False)
