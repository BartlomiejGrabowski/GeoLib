'''
Created on Jul 19, 2012

@author: bartek
@version: 1.0.0
@contact: bartlomiej.grabowski@tlen.pl
@requires: Python in version 2.6 and upper.
'''
import math
import sys
import os

class LatitudeRangeException(Exception):
    """Raises when latitude is not in the range (-90, +90)."""
    def __init__(self, message):
        self.message = message
        
class LongitudeRangeException(Exception):
    """Raises when longitude is not in the range (-180, +180)."""
    def __init__(self, message):
        self.message = message
        
class Geo(object):
    """Geo class provides a set of methods to calculating some geo-based parameters using 
        Python's built-in math library."""


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def distance_haversine(self, lat1, lon1, lat2, lon2):
        """ @brief Compute distance between two points in km using haversine formula.
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point.
            @return float Distance between source and destination point. """
        R = 6371.0
        
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            Lat = math.radians(lat2 - lat1)
            Lon = math.radians(lon2 - lon1)
            
            a = math.sin(Lat/2.0) * math.sin(Lat/2.0) + \
                math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
                math.sin(Lon/2.0) * math.sin(Lon/2.0)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1
        
        return (R * c)
    
    def distance_sloc(self, lat1, lon1, lat2, lon2):
        """ @brief Compute distance between two points in km using
            spherical law of cosines formula.
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point.
            @return float Distance between source and destination point. """
        R = 6371.0
        
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        try:
            c = math.acos(math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + \
                          math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
                          math.cos(math.radians(lon2 - lon1)))
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1
         
        return (R * c)
    
    def initial_bearing(self, lat1, lon1, lat2, lon2):
        """ @brief Bearing from one point to another in degrees (0-360).
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point.
            @return float Initial bearing between two points."""
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            lat1 = math.radians(lat1)
            lat2 = math.radians(lat2)
            lon1 = math.radians(lon1)
            lon2 = math.radians(lon2)
            dLon = lon2 - lon1
            
            y = math.sin(dLon) * math.cos(lat2)
            x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * \
                math.cos(lat2) * math.cos(dLon)
            brng = math.atan2(y, x)
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1 
        #Since atan2 returns values in the range -pi ... +pi (that is, -180 ... +180), 
        #to normalize the result to a compass bearing (in the range 0 ... 360...    
        return (math.degrees(brng) + 360) % 360
    
    def final_bearing(self, lat1, lon1, lat2, lon2):
        """ @brief Bearing from one point to another in degrees (0-360).
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point.
            @return float Final bearing between two points."""
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            lat1 = math.radians(lat1)
            lat2 = math.radians(lat2)
            lon1 = math.radians(lon1)
            lon2 = math.radians(lon2)
            dLon = lon2 - lon1
            
            y = math.sin(dLon) * math.cos(lat2)
            x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * \
                math.cos(lat2) * math.cos(dLon)
            brng = math.atan2(y, x)
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1 
        #Since atan2 returns values in the range -pi ... +pi (that is, -180 ... +180), 
        #to normalize the result to a compass bearing (in the range 0 ... 360...    
        return (math.degrees(brng) + 180) % 360
    
    def midpoint(self, lat1, lon1, lat2, lon2):
        """ @brief This is the half-way point along a great circle
            path between the two points.
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point.
            @return {lat3/lon3} float: Midpoint coordinates."""
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            lat1 = math.radians(lat1)
            lon1 = math.radians(lon1)
            lat2 = math.radians(lat2)
            lon2 = math.radians(lon2)
            
            bx = math.cos(lat2) * math.cos(lon2 - lon1)
            by = math.cos(lat2) * math.sin(lon2 - lon1)
            
            mLat = math.atan2(math.sin(lat1) + math.sin(lat2), \
                            math.sqrt((math.cos(lat1) + bx) * \
                            (math.cos(lat1) + bx) + by * by))
            mLon = lon1 + math.atan2(by, math.cos(lat1) + bx)
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1   
        
        return [round(math.degrees(mLat), 2), round(math.degrees(mLon), 2)]
    
    def intersection(self, lat1, lon1, brng1, lat2, lon2, brng2):
        """ @brief Intersection of two paths given start points and bearings.
            @param {lat1/lon1} float: Source point.
            @param brng1 float: Initial bearing from source point.
            @param {lat2/lon2} float: Destination point.
            @param brng2 float: Initial bearing from destination point.
            @return {lat3/lon3} float: Point of intersection of two path defined by point and bearing."""
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try: 
            lat1 = math.radians(lat1)
            lon1 = math.radians(lon1)
            lat2 = math.radians(lat2)
            lon2 = math.radians(lon2)
            
            dLat = lat2 - lat1
            dLon = lon2 - lon1
            
            brng1 = math.radians(brng1)
            brng2 = math.radians(brng2)
            
            d = 2 * math.asin(math.sqrt(math.sin(dLat/2) * math.sin(dLat/2) + \
                           math.cos(lat1) * math.cos(lat2) * \
                           math.sin(dLon/2) * math.sin(dLon/2)))
            
            if d == 0:
                return 0
            
            f1 = math.acos((math.sin(lat2) - math.sin(lat1) * math.cos(d)) / (math.sin(d) * math.cos(lat1)))
            
            #Protect against rounding.
            if math.isnan(f1):
                f1 = 0
                
            f2 = math.acos((math.sin(lat1) - math.sin(lat2) * math.cos(d)) / (math.sin(d) * math.cos(lat2)))
            
            if math.sin(lon2 - lon1) > 0:
                b1 = f1
                b2 = 2 * math.pi - f2
            else:
                b1 = 2 * math.pi - f1
                b2 = f2
                
            a1 = (brng1 - b1 + math.pi) % (2 * math.pi) - math.pi
            a2 = (b2 - brng2 + math.pi) % (2 * math.pi) - math.pi
            
            #Infinite intersections.
            if math.sin(a1) == 0 and math.sin(a2) == 0:
                return 0
            
            #Ambiguous intersection.
            if math.sin(a1) * math.sin(a2) < 0:
                return 0
            
            a3 = math.acos(-math.cos(a1) * math.cos(a2) + math.sin(a1) * math.sin(a2) * \
                           math.cos(d))
            
            dx = math.atan2(math.sin(d) * math.sin(a1) * math.sin(a2), \
                            math.cos(a2) + math.cos(a1) * math.cos(a3))
            
            lat3 = math.asin(math.sin(lat1) * math.cos(dx) + math.cos(lat1) * \
                             math.sin(dx) * math.cos(brng1))
            
            dLon13 = math.atan2(math.sin(brng1) * math.sin(dx) * math.cos(lat1), \
                                math.cos(dx) - math.sin(lat1) * math.sin(lat3))
            
            #lon3 = lon1 + dLon13
            #Normalise to -180...+180.
            #lon3 = (lon3 +3 * math.pi) % (2 * math.pi) - math.pi
            lon3 = (lon1 + dLon13 + math.pi) % (2 * math.pi) - math.pi
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1 
        return [math.degrees(lat3), math.degrees(lon3)]
    
    def rhumb_distance(self, lat1, lon1, lat2, lon2):
        """ @brief Returns the distance from point to the supplied point, 
            in km, traveling along a rhumb line.
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point
            @return distance float: Returns distance traveling along rhumb line."""
        R = 6371.0
        
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            lat1 = math.radians(lat1)
            lat2 = math.radians(lat2)
            lon1 = math.radians(lon1)
            lon2 = math.radians(lon2)
            
            dLat = lat2 - lat1
            dLon = math.fabs(lon2 - lon1)
            
            dPhi = math.log(math.tan(lat2/2 + math.pi/4)/math.tan(lat1/2 + math.pi/4))
            #E-W line gives dPhi=0.
            if math.isinf(dLat/dPhi):
                q = math.cos(lat1)
            else:
                q = dLat/dPhi
            
            #If dLon over 180 take shorter rhumb across 180 meridian.
            if math.fabs(dLon) > math.pi:
                if dLon > 0:
                    dLon = -(2 * math.pi - dLon)
                else:
                    dLon = 2 * math.pi + dLon
                    
            dist = math.sqrt(math.pow(dLat, 2) + math.pow(q, 2) * math.pow(dLon, 2)) * R
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1 
        
        return dist
    
    def rhumb_bearing(self, lat1, lon1, lat2, lon2):
        """ @brief Returns the bearing from this point to the supplied point along rhumb line, in degrees.
            @param {lat1/lon1} float: Coordinates of source point.
            @param {lat2/lon2} float: Coordinates of destination point.
            @return float: Bearing in degrees from North."""
        if (lat1 > 90 or lat1 < -90) or (lat2 > 90 or lat2 < -90):
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if (lon1 > 180 or lon1 < -180) or (lon2 > 180 or lon2 < -180):
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            lat1 = math.radians(lat1)
            lat2 = math.radians(lat2)
            lon1 = math.radians(lon1)
            lon2 = math.radians(lon2)
            
            dLon = lon2 - lon1
            dPhi = math.log(math.tan(lat2/2 + math.pi/4)/math.tan(lat1/2 + math.pi/4))
            
            #E-W line gives dPhi=0.
            if math.fabs(dLon) > math.pi:
                if dLon > 0:
                    dLon = -(2 * math.pi - dLon)
                else:
                    dLon = 2 * math.pi + dLon
            
            brng = math.atan2(dLon, dPhi)
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1
        
        return (math.degrees(brng) + 360) % 360
    
    def rhumb_destination_point(self, lat1, lon1, brng, dist):
        """ @brief Returns the destination point from this point having traveled the given
            distance (in km) on the given bearing along a rhumb line.
            @param lat1/lon1 float: Latitude/longitude of source point.
            @param brng float: Bearing in degrees from North.
            @param dist float: Distance in km.
            @return {Lat/Lon} float Destination point."""        
        R = 6371.0
        
        if lat1 > 90 or lat1 < -90: 
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if lon1 > 180 or lon1 < -180:
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            #Angular distance covered on earth's surface.
            d = float(dist)/R
            lat1 = math.radians(lat1)
            lon1 = math.radians(lon1)
            brng = math.radians(brng)
            
            lat2 = lat1 + d * math.cos(brng)
            dLat = lat2 - lat1
    
            dPhi = math.log(math.tan(lat2/2 + math.pi/4)/math.tan(lat1/2 + math.pi/4))
            
            #E-W line gives dPhi=0.
            if math.isinf(dLat/dPhi):
                q = math.cos(lat1)
            else:
                q = dLat/dPhi
                
            dLon = d * math.sin(brng)/q
            if math.fabs(lat2) > math.pi/2.0:
                if lat2 > 0:
                    lat2 = math.pi - lat2
                else:
                    lat2 = -math.pi - lat2
            
            lon2 = (lon1 + dLon + 3 * math.pi) % (2 * math.pi) - math.pi
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1
        return [math.degrees(lat2), math.degrees(lon2)]
    
    def rhumb_midpoint(self, lat1, lon1, lat2, lon2):
        """ @brief Returns the loxodromic midpoint (along a rhumb line) between 
            this point and the supplied point.
            @param {lat1/lon1} float: Source point.
            @param {lat2/lon2} float: Destination point.
            @return {Lat/Lon} float: Midpoint between this point and the supplied point."""
            
        if lat1 > 90 or lat1 < -90: 
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if lon1 > 180 or lon1 < -180:
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            lat1 = math.radians(lat1)
            lat2 = math.radians(lat2)
            lon1 = math.radians(lon1)
            lon2 = math.radians(lon2)
            
            lat3 = (lat2 + lat1)/2.0
            f1 = math.tan(math.pi/4.0 + lat1/2.0)
            f2 = math.tan(math.pi/4.0 + lat2/2.0)
            f3 = math.tan(math.pi/4.0 + lat3/2.0)
            
            lon3 = ((lon2 - lon1) * math.log(f3) + lon1 * math.log(f2) - lon2 * \
                    math.log(f1)) / math.log(f2/f1)
                    
            if math.isnan(lon3):
                lon3 = (lon1 + lon2)/2.0
                
            #Normalize to -180 .. 180.
            lon3 = (lon3 + 3 * math.pi) % (2 * math.pi) - math.pi
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1
        
        return [math.degrees(lat3), math.degrees(lon3)]
    
    def destination_point(self, lat1, lon1, brng, dist):
        """ @brief Returns the destination point from source point.
            @param {lat1/lon1} float: Latitude/Longitude of source point.
            @param brng float: Initial bearing in degrees.
            @param dist float: Distance in km.
            @return {lat2/lon2} float: Destination point."""
        R = 6371.0
        
        if lat1 > 90 or lat1 < -90: 
            raise LatitudeRangeException("Latitude exceeds the range (-90 .. 90)")
        if lon1 > 180 or lon1 < -180:
            raise LongitudeRangeException("Longitude exceeds the range (-180 .. 180)")
        
        try:
            #Convert distance to angular distance in radians.
            dist = dist/R 
            lat1 = math.radians(lat1)
            lon1 = math.radians(lon1)
            brng = math.radians(brng)
            
            lat2 = math.asin(math.sin(lat1) * math.cos(dist) + math.cos(lat1) * \
                             math.sin(dist) * math.cos(brng))
            lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(dist) * math.cos(lat1), \
                                     math.cos(dist) - math.sin(lat1) * math.sin(lat2))
            #Normalize to -180 .. 180.
            lon2 = (lon2 + 3* math.pi) % (2 * math.pi) - math.pi
        except Exception as ex:
            sys.stderr.write('ERROR: %s\n' % str(ex))
            return 1
        
        return [math.degrees(lat2), math.degrees(lon2)]
        
if __name__ == '__main__':
    #Simple using tests
    
    g = Geo()
    print('Using tests')
    print(g.distance_haversine(53.123, 21.020, 54.520, 18.530))
    print(g.distance_sloc(52.259, 21.020, 54.520, 18.530))
    print(g.initial_bearing(50.0359, 5.4255, 58.38, 3.042))
    print(g.final_bearing(50.0359, 5.4255, 58.38, 3.042))
    print(g.midpoint(34.122222, 118.4111111, 40.66972222, 73.94388889))
    print(g.intersection(51.885, 0.235, 108.63, 49.008, 2.549, 32.72))
    print(g.rhumb_distance(50.2150, 4.0925, 42.2104, 71.0227))
    print(g.rhumb_bearing(50.2150, 4.0925, 42.2104, 71.0227))
    print(g.rhumb_destination_point(51.0732, 1.2017, 116.3810, 40.23))
    print(g.rhumb_midpoint(50.2150, 4.0925, 42.2104, 71.0227))
    print(g.destination_point(53.1914, 1.4347, 96.0118, 124.8))
    