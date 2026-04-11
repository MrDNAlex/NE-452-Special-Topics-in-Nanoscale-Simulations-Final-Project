from ParseXYZ import Parse as ParseXYZ
from ParseSinglePoint import Parse as ParseSinglePoint
from ParseGeoOpts import Parse as ParseGeoOpts
from ParseTiming import Parse as ParseTiming
from CalculateFinalEnthalpy import Parse as ParseFinalEnthalpy
from CompareFinalEnthalpy import Compare as CompareFinalEnthalpy

# Run all the Parsing all in one go in the proper order
ParseXYZ()
ParseSinglePoint()
ParseGeoOpts()
ParseTiming()
ParseFinalEnthalpy()
CompareFinalEnthalpy()