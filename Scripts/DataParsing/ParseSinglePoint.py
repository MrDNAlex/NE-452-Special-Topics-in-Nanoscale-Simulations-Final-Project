from ncl.Orca import OrcaOutputFile
from Data import FUNCTIONALS, ATOMS, HARTREE_TO_KJMOL
import pandas as pd
import os

def Parse():
    T = 298.15

    def getEnthalpyHartrees(tempK: float):
        R = 8.314 
        return float(5/2) * R * tempK / (HARTREE_TO_KJMOL * 1000.0)

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

    # Write the Data Frame
    for atom in ATOMS.keys():
        row = [atom]
        
        for func in FUNCTIONALS:
            # Find the Appropriate file in the proper order, add the Final Single Point Energy to the row
            filePath = next((f for f in outputFiles[atom] if func in f), None)
            row.append(OrcaOutputFile(filePath).getFinalEnergy())
        
        dataFrame.loc[len(dataFrame)] = row

    experimentalCorrection = pd.read_csv("Results/ExperimentalCorrections.csv")

    # Add the Experimental Enthalpy Corrections to reference later
    dataFrame["Experimental Enthalpy Correction"] = experimentalCorrection["Experimental Enthalpy Correction (Eh)"]

    # Add the Enthalpy Correction to all columns
    dataFrame["Thermal Enthalpy Correction"] = [getEnthalpyHartrees(T) for i in range(len(dataFrame))]

    for i in range(len(FUNCTIONALS)):
        energyColumn = dataFrame[dataFrame.columns[i+1]]
        dataFrame[f"{FUNCTIONALS[i]} Enthalpy"] = energyColumn.values + dataFrame["Thermal Enthalpy Correction"].values

    print(dataFrame)
    dataFrame.to_csv("Results/AtomEnthalpies.csv", index=False)

if __name__ == "__main__":
    Parse()