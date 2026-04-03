from Data import FUNCTIONALS, MOLECULES, ATOMS
import pandas as pd

def Parse():
    # Load the Reference DataFrames
    enthalpyDataFrame = pd.read_csv("Results/MoleculeEnthalpies.csv")
    xyzDataFrame = pd.read_csv("Results/AtomCount.csv")
    atomEnthalpiesDataFrame = pd.read_csv("Results/AtomEnthalpies.csv")

    masterDataFrame = enthalpyDataFrame.copy()

    # Add a Column for the Number of certain Atoms in each molecule
    # 
    # Multiply the Atomic Enthalpies by the number of Atoms contained in the molecule
    for i in range(1, len(xyzDataFrame.columns)):
        columnName = xyzDataFrame.columns[i]
        atomName = columnName.split()[0]
        enthalpyCorrectionColumnName = f"{atomName} Enthalpy Correction" 
        
        # Add number of Atoms per molecule of certain type
        masterDataFrame[columnName] = xyzDataFrame[columnName]
        
        # Add the experimental Correction Enthalpy
        masterDataFrame[enthalpyCorrectionColumnName] = masterDataFrame[columnName] * atomEnthalpiesDataFrame["Experimental Enthalpy Correction"][ATOMS[atomName]]
        
        # Calaculate the total enthalpy contribution for a certain atom
        for func in FUNCTIONALS:
            enthalpyColumnName = f"Final {atomName} {func} Enthalpy"
            functionalEnthalpy = atomEnthalpiesDataFrame[f"Final Atom {func} Enthalpy"] 
    
            masterDataFrame[enthalpyColumnName] = masterDataFrame[columnName] * functionalEnthalpy[ATOMS[atomName]]

    # Subtract Sum of the Total Enthalpy Contribution of each Atom from the Total Molecule Enthalpy to get Formation
    for i in range(len(FUNCTIONALS)):
        func = FUNCTIONALS[i]
        elementSums = [0 for _ in range(len(MOLECULES))]
        
        for atom in ATOMS.keys():
            elementSums += masterDataFrame[f"Final {atom} {func} Enthalpy"]
        
        masterDataFrame[f"{func} Enthalpy of Formation"] = masterDataFrame[masterDataFrame.columns[1 + i]] - elementSums
            
    print(masterDataFrame)
    masterDataFrame.to_csv("Results/MasterEnthalpies.csv", index=False)

if __name__ == "__main__":
    Parse()