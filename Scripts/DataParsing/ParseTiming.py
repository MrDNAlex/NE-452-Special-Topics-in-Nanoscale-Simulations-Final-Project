from ncl.Orca import OrcaOutputFile
from Data import FUNCTIONALS, MOLECULES
import pandas as pd
import os

def Parse():
    # Initialize the Data Frame
    dataFrame = pd.DataFrame(
        columns=["Molecule Name", "LDA Time (s)", "PBE Time (s)", "B3LYP Time (s)", "wB97x-D3 Time (s)", "M06-2X Time (s)"]
    )

    # Create a Dictionary for the Output Files
    outputFiles = {}

    # Find the Output files
    for path, dirs, files in os.walk("Data\\GeoOpt"):

        if len(files) == 0:
            continue

        moleculeName = path.split("\\")[-1]
        
        # Initialize the nested dictionary for this molecule
        if moleculeName not in outputFiles:
            outputFiles[moleculeName] = {func: [] for func in FUNCTIONALS}

        for file in files:
            if not file.endswith(".out"):
                continue
                
            # Match the file to its corresponding functional
            for func in FUNCTIONALS:
                if func in file:
                    filePath = os.path.join(path, file)
                    outputFiles[moleculeName][func].append(filePath)
                    break

    # Write the Data Frame
    for mol in MOLECULES:
        if mol not in outputFiles:
            continue
            
        row = [mol]
        
        for func in FUNCTIONALS:
            functionalTotalTime = 0.0
            
            # Loop through all iteration files for this specific functional and sum their times
            for filePath in outputFiles[mol][func]:
                calc = OrcaOutputFile(filePath)
                functionalTotalTime += calc.getTotalTime() 
                    
            row.append(functionalTotalTime)
        
        dataFrame.loc[len(dataFrame)] = row
            
    print(dataFrame)
    dataFrame.to_csv("Results/MoleculeTimings.csv", index=False)
    
if __name__ == "__main__":
    Parse()