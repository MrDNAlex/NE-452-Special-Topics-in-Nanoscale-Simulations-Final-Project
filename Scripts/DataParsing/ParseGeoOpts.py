from ncl.Orca import OrcaOutputFile
from Data import FUNCTIONALS, MOLECULES
import pandas as pd
import os

# Initialize the Data Frame
dataFrame = pd.DataFrame(
    columns=["Molecule Name", "LDA Enthalpy", "PBE Enthalpy", "B3LYP Enthalpy", "wB97x-D3 Enthalpy", "M06-2X Enthalpy"]
)

# Create a Dictionary for the Output Files
outputFiles = {}

# Find the Last GeoOpt Output files
for path, dirs, files in os.walk("Data\\GeoOpt"):

    if len(files) == 0:
        continue

    moleculeName = path.split("\\")[-1]
    outputFiles[moleculeName] = []

    # Case where some GeoOpts had to run Multiple Times
    if len(files) > 5:
        for file in files:
            
            # Extract the Suffix and Index of the file
            fileSuffix = file.split(".")[0][:-1]
            index = int(file.split("-")[-1].split(".")[0])

            # Iterate until no file is found
            while fileSuffix + f"{index + 1}.out" in files:
                index += 1

            outputFiles[moleculeName].append(os.path.join(path, fileSuffix + f"{index}.out"))

        continue

    # Add the files outright because no files are found
    for file in files:
        outputFiles[moleculeName].append(os.path.join(path, file))

# Write the Data Frame
for mol in MOLECULES:    
    row = [mol]
    
    for func in FUNCTIONALS:
        # Find the Appropriate file in the proper order, add the Total Enthalpy to the row
        filePath = next((f for f in outputFiles[mol] if func in f), None)
        row.append(OrcaOutputFile(filePath).totalEnthalpy)
    
    dataFrame.loc[len(dataFrame)] = row
        
print(dataFrame)
dataFrame.to_csv("Results/MoleculeEnthalpies.csv", index=False)
    