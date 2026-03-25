from ProDrug.GeoOptAcetaminophen import runGeoOpt as runGeoOptAcetaminophen
from ProDrug.GeoOptDexamethasone import runGeoOpt as runGeoOptDexamethasone
from ProDrug.GeoOptDiclofenac import runGeoOpt as runGeoOptDiclofenac
from ProDrug.GeoOptHydrocortisone import runGeoOpt as runGeoOptHydrocortisone
from ProDrug.GeoOptIbuprofen import runGeoOpt as runGeoOptIbuprofen
from ProDrug.GeoOptPrednisone import runGeoOpt as runGeoOptPrednisone

# Run Alkane GeoOpts
def RunProDrugGeoOpt():
    runGeoOptAcetaminophen()
    runGeoOptDexamethasone()
    runGeoOptDiclofenac()
    runGeoOptHydrocortisone()
    runGeoOptIbuprofen()
    runGeoOptPrednisone()
    
if __name__ == "__main__":
    RunProDrugGeoOpt()