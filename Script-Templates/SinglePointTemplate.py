from ncl import Molecule
from ncl.Orca import OrcaInputFile, OrcaDockerCalculation, OrcaCalculation
import time

def runSinglePoint():
    cores = 8
    moleculeName = "MoleculeName"
    moleculePath = "path/to/molecule.xyz"
    functionals = ["LDA", "PBE", "B3LYP", "wB97X-D3", "M062X"]
    basis = "DEF2-SVP"
    
    start = time.time()

    for func in functionals:
        molecule = Molecule(f"{moleculeName}-{func}", moleculePath, mult=3)
        inputFile = OrcaInputFile(f"{moleculeName}-{func}", molecule)
        inputFile.addRoute(func)
        inputFile.addRoute(basis)
        inputFile.addRoute("TightSCF")
        inputFile.addRoute("DefGrid3")
        inputFile.addRoute(f"PAL{cores}")
        
        calculation = OrcaDockerCalculation(inputFile)
        calcResults = calculation.calculate()
        print(calcResults.status)
        
    calcResults.elapsed = time.time() - start
    print(f"SinglePoint finished in : {calcResults.getCalculationTime()}")

if __name__ == "__main__":
    runSinglePoint()