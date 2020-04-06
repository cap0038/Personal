'''
    Created on March 28th, 2019

    @author:    Cait Potridge
'''
import math

def correct(values=None):
    if (not('lat' in values) or not('long' in values) or not('altitude' in values) or not('assumedLat' in values) or not('assumedLong' in values)):
        values['error'] = 'missing mandatory information'
        return values
     
    lat = values['lat']
    longValue = values['long']
    altitude = values['altitude']
    assumedLat = values['assumedLat']
    assumedLong = values['assumedLong']
    
    placeOfD = lat.find('d')
    if (placeOfD != -1):    
        latX = lat[:placeOfD]
        latY = lat[(placeOfD+1):]
        try:
            latX = int(latX)
            latY = float(latY)
        except:
            values['error'] = 'invalid lat'
            return values
    else:    
        values['error'] = 'invalid lat'
        return values
    
    placeOfD = longValue.find('d')
    if (placeOfD != -1):    
        longX = longValue[:placeOfD]
        longY = longValue[(placeOfD+1):]
        try:
            longX = int(longX)
            longY = float(longY)
        except:
            values['error'] = 'invalid long'
            return values
    else:    
        values['error'] = 'invalid long'
        return values
     
    placeOfD = altitude.find('d')
    if (placeOfD != -1):    
        altitudeX = altitude[:placeOfD]
        altitudeY = altitude[(placeOfD+1):]
        try:
            altitudeX = int(altitudeX)
            altitudeY = float(altitudeY)
        except:
            values['error'] = 'invalid altitude'
            return values
    else:    
        values['error'] = 'invalid altitude'
        return values
     
    placeOfD = assumedLat.find('d')
    if (placeOfD != -1):    
        assumedLatX = assumedLat[:placeOfD]
        assumedLatY = assumedLat[(placeOfD+1):]
        try:
            assumedLatX = int(assumedLatX)
            assumedLatY = float(assumedLatY)
        except:
            values['error'] = 'invalid assumedLat'
            return values
    else:    
        values['error'] = 'invalid assumedLat'
        return values
     
    placeOfD = assumedLong.find('d')
    if (placeOfD != -1):    
        assumedLongX = assumedLong[:placeOfD]
        assumedLongY = assumedLong[(placeOfD+1):]
        try:
            assumedLongX = int(assumedLongX)
            assumedLongY = float(assumedLongY)
        except:
            values['error'] = 'invalid assumedLong'
            return values
    else:    
        values['error'] = 'invalid assumedLong'
        return values
    
    lat = latX + (latY / 60)
    if (lat < -90 or lat > 90):
        values['error'] = 'invalid lat'
        return values
    
    longValue = longX + (longY / 60)
    if (longValue < 0 or longValue > 360):
        values['error'] = 'invalid long'
        return values
    
    altitude = altitudeX + (altitudeY / 60)
    if (altitude < 0 or altitude > 90):
        values['error'] = 'invalid altitude'
        return values
    
    assumedLat = assumedLatX + (assumedLatY / 60)
    if (assumedLat < -90 or assumedLat > 90):
        values['error'] = 'invalid assumedLat'
        return values
    
    assumedLong = assumedLongX + (assumedLongY / 60)
    if (assumedLong < 0 or assumedLong > 360):
        values['error'] = 'invalid assumedLong'
        return values
    
    calculationList = calculateCorrectedValues(lat, longValue, altitude, assumedLat, assumedLong)

    values['correctedDistance'] = calculationList[0]
    values['correctedAzimuth'] = calculationList[1]
    
    return values

def calculateCorrectedValues(latIn, longIn, altitudeIn, assumedLatIn, assumedLongIn):
    LHA = longIn + assumedLongIn
    LHA = LHA % 360
            
    intermediateDistance = ((math.sin(math.radians(latIn)) * math.sin(math.radians(assumedLatIn))) + (math.cos(math.radians(latIn)) * math.cos(math.radians(assumedLatIn)) * math.cos(math.radians(LHA))))
    
    correctedAltitude = math.asin(intermediateDistance)
    correctedAltitude = correctedAltitude * (180/math.pi)
    
    correctedDistance = altitudeIn - correctedAltitude
    correctedDistance = int(round(correctedDistance * 60))
    
    correctedAzimuth = math.acos((math.sin(math.radians(latIn)) - (math.sin(math.radians(assumedLatIn)) * intermediateDistance)) / (math.cos(math.radians(assumedLatIn)) * math.cos(math.radians(correctedAltitude))))
    correctedAzimuth = correctedAzimuth * (180/math.pi)
    
    if (correctedDistance < 0):
        correctedDistance = abs(correctedDistance)
        correctedAzimuth += 180
        correctedAzimuth = correctedAzimuth % 360
            
    correctedAzimuth = str(int(correctedAzimuth)) + 'd' + str(round(((correctedAzimuth - int(correctedAzimuth)) * 60), 1))
    
    return [str(correctedDistance), correctedAzimuth] 