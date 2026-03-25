from Alkanes.GeoOptMethane import runGeoOpt as runGeoOptMethane
from Alkanes.GeoOptEthane import runGeoOpt as runGeoOptEthane
from Alkanes.GeoOptPropane import runGeoOpt as runGeoOptPropane
from Alkanes.GeoOptButane import runGeoOpt as runGeoOptButane
from Alkanes.GeoOptPentane import runGeoOpt as runGeoOptPentane
from Alkanes.GeoOptHexane import runGeoOpt as runGeoOptHexane
from Alkanes.GeoOptHeptane import runGeoOpt as runGeoOptHeptane
from Alkanes.GeoOptOctane import runGeoOpt as runGeoOptOctane
from Alkanes.GeoOptNonane import runGeoOpt as runGeoOptNonane

# Run Alkane GeoOpts
def RunAlkaneGeoOpt():
    runGeoOptMethane()
    runGeoOptEthane()
    runGeoOptPropane()
    runGeoOptButane()
    runGeoOptPentane()
    runGeoOptHexane()
    runGeoOptHeptane()
    runGeoOptOctane()
    runGeoOptNonane()
    
if __name__ == "__main__":
    RunAlkaneGeoOpt()