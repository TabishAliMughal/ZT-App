from math import sin, cos, sqrt, atan2, radians
import haversine as hs



def LatLonCalculator(loc1,loc2):
    t = hs.haversine(loc1,loc2)
    return t