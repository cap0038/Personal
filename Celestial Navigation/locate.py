'''
    Created on April 30th, 2019

    @author:    Cait Potridge
'''

import math
def locate(values=None):
    if (not('assumedLat' in values)):
        values['error'] = 'assumedLat is missing'
        return values
    if (not('assumedLong' in values)):
        values['error'] = 'assumedLong is missing'
        return values
    if (not('corrections' in values)):
        values['error'] = 'corrections is missing'
        return values
    
    assumedLat = values['assumedLat']
    assumedLong = values['assumedLong']
    corrections = values['corrections']
    distanceList = []
    azimuthList = []
    azimuthTempList = []
    distanceTempList = []
    
    try:
        strs = corrections.replace('[','').split('],')
        corrections = [map(str, s.replace(']','').split(',')) for s in strs]
    except: 
        values['error'] = 'invalid corrections'
        return values

    for sublist in corrections: 
        try:
            distanceTempList.append(sublist[0])
            azimuthTempList.append(sublist[1])
        except: 
            values['error'] = 'invalid corrections'
            return values
        
    for azimuth in azimuthTempList:
        if 'd' not in azimuth:
            values['error'] = 'invalid corrections'
            return values
        else:
            placeOfD = azimuth.find('d')
            if (placeOfD != -1):    
                azimuthX = azimuth[:placeOfD]
                azimuthY = azimuth[(placeOfD+1):]
                try:
                    azimuthX = int(azimuthX)
                    azimuthY = round(float(azimuthY), 1)
                    if(azimuthY >= 60 or azimuthY < 0):
                        values['error'] = 'invalid corrections'
                        return values
                except:
                    values['error'] = 'invalid corrections'
                    return values
            else:    
                values['error'] = 'invalid corrections'
                return values
            
            azimuth = azimuthX + (azimuthY / 60)
            if (azimuth < 0 or azimuth >= 360):
                values['error'] = 'invalid corrections'
                return values
            azimuthList.append(azimuth)
            
    for distance in distanceTempList:
        try:
            dist = int(distance)
            if (dist < 0):
                values['error'] = 'invalid corrections'
                return values
            else:
                distanceList.append(dist)
        except:
            values['error'] = 'invalid corrections'
            return values
        
    placeOfD = assumedLat.find('d')
    if (placeOfD != -1):    
        assumedLatX = assumedLat[:placeOfD]
        assumedLatY = assumedLat[(placeOfD+1):]
        try:
            assumedLatX = int(assumedLatX)
            assumedLatY = round(float(assumedLatY), 1)
            if(assumedLatY >= 60 or assumedLatY < 0):
                values['error'] = 'invalid assumedLat'
                return values
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
            assumedLongY = round(float(assumedLongY), 1)
            if(assumedLongY >= 60 or assumedLongY < 0):
                values['error'] = 'invalid assumedLong'
                return values
        except:
            values['error'] = 'invalid assumedLong'
            return values
    else:    
        values['error'] = 'invalid assumedLong'
        return values
    
    assumedLat = assumedLatX + (assumedLatY / 60)
    if (assumedLat <= -90 or assumedLat >= 90):
        values['error'] = 'invalid assumedLat'
        return values
    
    assumedLong = assumedLongX + (assumedLongY / 60)
    if (assumedLong < 0 or assumedLong >= 360):
        values['error'] = 'invalid assumedLong'
        return values
    
    calculationList = calculateCorrections(assumedLat, assumedLong, azimuthList, distanceList)
    values['presentLat'] = calculationList[0]
    values['presentLong'] = calculationList[1]
    values['precision'] = calculationList[2]
    
    return values

def calculateCorrections(assumedLa, assumedLo, correctAzimuth, correctDistance):
    cosCorrectAzimuth = []
    sinCorrectAzimuth = []
    cosSquares = []
    sinSquares = []
    precisionTotal = []
    
    for azimuth in correctAzimuth:
        cosCorrectAzimuth.append(math.cos(math.radians(azimuth)))
        sinCorrectAzimuth.append(math.sin(math.radians(azimuth)))
        
    nsCorrection = (sum(x * y for x,y in zip(correctDistance, cosCorrectAzimuth))) / (len(correctDistance))    
    ewCorrection = (sum(x * y for x,y in zip(correctDistance, sinCorrectAzimuth))) / (len(correctDistance))
    
    presentLat = assumedLa + nsCorrection / 60
    presentLong = assumedLo + ewCorrection / 60
    
    presentLat = str(int(presentLat)) + 'd' + str(round(((presentLat - int(presentLat)) * 60), 1))
    presentLong = str(int(presentLong)) + 'd' + str(round(((presentLong - int(presentLong)) * 60), 1))
    
    for d,aC,aS in zip(correctDistance, cosCorrectAzimuth, sinCorrectAzimuth):
        cosSquares.append((d * aC - float(nsCorrection)) ** 2)
        sinSquares.append((d * aS - float(ewCorrection)) ** 2)
        
    for c,s in zip(cosSquares, sinSquares):
        precisionTotal.append(math.sqrt(c + s))
        
    precision = (1.0/(len(correctDistance))) * (sum(precisionTotal))
    
    return presentLat, presentLong, str(int(precision))