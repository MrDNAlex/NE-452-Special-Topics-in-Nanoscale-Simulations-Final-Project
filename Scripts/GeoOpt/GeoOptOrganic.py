from Organic.GeoOptAspirin import runGeoOpt as runGeoOptAspirin
from Organic.GeoOptAzobenzene import runGeoOpt as runGeoOptAzobenzene
from Organic.GeoOptCaffeine import runGeoOpt as runGeoOptCaffeine
from Organic.GeoOptEthanol import runGeoOpt as runGeoOptEthanol
from Organic.GeoOptPyrrole import runGeoOpt as runGeoOptPyrrole

# Run Alkane GeoOpts
def RunOrganicGeoOpt():
    runGeoOptAspirin()
    runGeoOptAzobenzene()
    runGeoOptCaffeine()
    runGeoOptEthanol()
    runGeoOptPyrrole()
    
if __name__ == "__main__":
    RunOrganicGeoOpt()