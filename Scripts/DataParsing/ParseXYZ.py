from ncl import Molecule
from Data import MOLECULES, ATOMS_ELEMENTS
import pandas as pd
import os


def Parse():
    # Initialize the Data Frame
    dataFrame = pd.DataFrame(
        columns=["Molecule Name", "Hydrogen Count", "Carbon Count", "Nitrogen Count", "Oxygen Count", "Fluorine Count", "Chlorine Count"]
    )

    xyzFiles = []

    # Find the path to the Single Point Output files
    for path, dirs, files in os.walk("Molecules\\Literature-XYZ"):

        if len(files) == 0:
            continue
        
        category = path.split("\\")[-1]

        # Add the files outright because no files are found
        for file in files:
            xyzFiles.append(os.path.join(path, file))

    # Write the Data Frame
    for mol in MOLECULES:    
        row = [mol]
        
        # Extract the file path and the Element Dictionary of the Atom
        filePath = next((f for f in xyzFiles if mol in f), None)
        elementDict = Molecule(mol, filePath).positions["Atom"].value_counts().to_dict()
        
        for element in ATOMS_ELEMENTS:
            if element in elementDict:
                row.append(elementDict[element])
            else:
                row.append(0)
        
        dataFrame.loc[len(dataFrame)] = row

    print(dataFrame)
    dataFrame.to_csv("Results/AtomCount.csv", index=False)

if __name__ == "__main__":
    Parse()