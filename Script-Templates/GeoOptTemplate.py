from ncl import Molecule
from ncl.Orca.Pipelines import OrcaGeoOpt

def runGeoOpt():
    cores = 8
    moleculeName = "molecule"
    moleculePath = "path/to/molecule.xyz"
    functionals = ["LDA", "PBE", "B3LYP", "wB97X-D3", "M062X"]
    basis = "DEF2-SVP"

    for func in functionals:
        molecule = Molecule(f"{moleculeName}-{func}", moleculePath)
        calculation = OrcaGeoOpt(molecule, func, basis, f"PAL{cores}", useDocker=False)
        calcResults = calculation.calculate()
        print(calcResults.status)

if __name__ == "__main__":
    runGeoOpt()
    