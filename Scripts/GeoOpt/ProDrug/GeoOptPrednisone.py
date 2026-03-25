from ncl import Molecule
from ncl.Orca.Pipelines import OrcaGeoOpt
import time

def runGeoOpt():
    cores = 8
    moleculeName = "Prednisone"
    moleculePath = "Molecules\Literature-XYZ\Pro-Drug\Prednisone.xyz"
    functionals = ["LDA", "PBE", "B3LYP", "wB97X-D3", "M062X"]
    basis = "DEF2-SVP"
    
    start = time.time()

    for func in functionals:
        molecule = Molecule(f"{moleculeName}-{func}", moleculePath)
        calculation = OrcaGeoOpt(molecule, func, basis, f"PAL{cores}", useDocker=True)
        calcResults = calculation.calculate()
        print(calcResults.status)
        
    calcResults.elapsed = time.time() - start
    print(f"All GeoOpts finished in : {calcResults.getCalculationTime()}")

if __name__ == "__main__":
    runGeoOpt()