from Data import FUNCTIONALS, MOLECULES, ATOMS
import pandas as pd

def Parse():
    # Load the Reference DataFrames
    enthalpyDataFrame = pd.read_csv("Results/MoleculeEnthalpies.csv")
    xyzDataFrame = pd.read_csv("Results/AtomCount.csv")
    atomEnthalpiesDataFrame = pd.read_csv("Results/AtomEnthalpies.csv")

    masterDataFrame = enthalpyDataFrame.copy()

    for i in range(1, len(xyzDataFrame.columns)):
        
        columnName = xyzDataFrame.columns[i]
        atomName = columnName.split()[0]
        enthalpyCorrectionColumnName = f"{atomName} Enthalpy Correction" 
        masterDataFrame[columnName] = xyzDataFrame[columnName]
        
        masterDataFrame[enthalpyCorrectionColumnName] = masterDataFrame[columnName] * atomEnthalpiesDataFrame["Experimental Enthalpy Correction"][ATOMS[atomName]]
        
        for func in FUNCTIONALS:
            enthalpyColumnName = f"{atomName} {func} Enthalpy" 
            functionalEnthalpies = atomEnthalpiesDataFrame[f"{func} Enthalpy"]
            
            masterDataFrame[enthalpyColumnName] = masterDataFrame[columnName] * functionalEnthalpies[ATOMS[atomName]]
            
    for i in range(len(FUNCTIONALS)):
    #for func in FUNCTIONALS:
        func = FUNCTIONALS[i]
        columnName = f"Final {func} Enthalpy"
        
        elementSums = [0 for _ in range(len(MOLECULES))]
        correctionSums = [0 for _ in range(len(MOLECULES))]
        
        for atom in ATOMS.keys():
            elementSums += masterDataFrame[f"{atom} {func} Enthalpy"]
            correctionSums += masterDataFrame[f"{atom} Enthalpy Correction"]
        
        masterDataFrame[columnName] = masterDataFrame[masterDataFrame.columns[1 + i]] - elementSums + correctionSums
            
    print(masterDataFrame)
    masterDataFrame.to_csv("Results/MasterEnthalpies.csv", index=False)

if __name__ == "__main__":
    Parse()