'''
    Created on March 5th, 2019

    @author:    Cait Potridge
'''
from datetime import datetime,date
import time

def predict(values=None):
    if (not('body' in values)):
        values['error'] = 'mandatory information is missing'
        return values
    
    if ((not('date' in values)) or (values['date'] == '')):
        dateIn = '2001-01-01'
    else:
        if(len(values['date']) == 10):
            dateIn = values['date']
        else:
            values['error'] = 'invalid date'
            return values
        
    if ((not('time' in values)) or (values['time'] == '')):
        timeIn = '00:00:00'
    else:
        if(len(values['time']) == 8):
            timeIn = values['time']
        else:
            values['error'] = 'invalid time'
            return values
        
    CELESTIAL_DICTIONARY = createCelestialDictionary() 
    bodyName = values['body']
    dateFormat = '%Y-%m-%d'
    timeFormat = '%H:%M:%S'
    
    if (not(bodyName in CELESTIAL_DICTIONARY)):
        values['error'] = 'star not in catalog'
        return values  
    
    try:
        validDate = datetime.strptime(dateIn, dateFormat).date()
        if (not(date(2001, 1, 1) <= validDate <= date(2100, 12, 31))):
            values['error'] = 'invalid date'
            return values
        validYear = validDate.year
    except ValueError:
        values['error'] = 'invalid date'
        return values
    
    try:
        validTime = datetime.strptime(timeIn, timeFormat).time()
    except:
        values['error'] = 'invalid time'
        return values
    
    latitude = CELESTIAL_DICTIONARY[bodyName][1]
    SHAStar = CELESTIAL_DICTIONARY[bodyName][0]
    
    placeOfD = SHAStar.find('d')
    degreesSHA = SHAStar[:placeOfD]
    minutesSHA = SHAStar[(placeOfD + 1):]
    degreesSHA = int(degreesSHA)
    minutesSHA = float(minutesSHA)
    SHAStar = degreesSHA + (minutesSHA / 60)
    
    finalGHA = calculateGHA(validYear, validDate, validTime) 
    finalGHA += SHAStar
    finalGHA %= 360
    GHADegree = int(finalGHA)
    GHAMinute = round(((finalGHA - int(finalGHA)) * 60), 1)
    finalGHA = str(GHADegree) + 'd' + str(GHAMinute) 
    
    values['lat'] = latitude
    values['long'] = finalGHA
    
    return values

def createCelestialDictionary():
    # Format: Key is name, followed by sidereal, declination, magnitude
    
    tempDictionary = {
        "Achernar": ['335d25.5', '-57d09.7', 0.5],
        "Acrux": ['173d07.2', '-63d10.9', 1.4],
        "Adara": ['255d10.8', '-28d59.9', 1.51],
        "Alcaid": ['152d57.8', '49d13.8', 1.8],
        "Aldebaran": ['290d47.1', '16d32.3', 0.85],
        "Alioth": ['166d19.4', '55d52.1', 1.76],
        "Alnair": ['27d42.0', '-46d53.1', 1.74],
        "Alnilam": ['275d44.3', '-1d11.8', 1.7],
        "Alphard": ['217d54.1', '-8d43.8', 2],
        "Alphecca": ['126d09.9', '26d39.7', 2.24],
        "Alpheratz": ['357d41.7', '29d10.9', 2.06],
        "Altair": ['62d06.9', '8d54.8', 0.77],
        "Ankaa": ['53d14.1', '-42d13.4', 2.37],
        "Antares": ['112d24.4', '-26d27.8', 1.09],
        "Arcturus": ['145d54.2', '19d06.2', -0.04],
        "Atria": ['107d25.2', '-69d03.0', 1.92],
        "Avior": ['234d16.6', '-59d33.7', 2.4],
        "Bellatrix": ['278d29.8', '6d21.6', 1.64],
        "Betelgeuse": ['270d59.1', '7d24.3', 0.58],
        "Canopus": ['263d54.8', '-52d42.5', -0.72],
        "Capella": ['280d31.4', '46d00.7', 0.71],
        "Deneb": ['49d30.7', '45d20.5', 1.25],
        "Denebola": ['182d31.8', '14d28.9', 2.14],
        "Diphda": ['348d54.1', '-17d54.1', 2.04],
        "Dubhe": ['193d49.4', '61d39.5', 1.87],
        "Elnath": ['278d10.1', '28d37.1', 1.68],
        "Enif": ['33d45.7', '9d57.0', 2.4],
        "Etamin": ['90d45.9', '51d29.3', 2.23],
        "Fomalhaut": ['15d22.4', '-29d32.3', 1.16],
        "Gacrux": ['171d58.8', '-57d11.9', 1.63],
        "Gienah": ['175d50.4', '-17d37.7', 2.8],
        "Hadar": ['148d45.5', '-60d26.6', 0.6],
        "Hamal": ['327d58.7', '23d32.3', 2],
        "Kaus Australis": ['83d41.9', '-34d22.4', 1.8],
        "Kochab": ['137d21.0', '74d05.2', 2.08],
        "Markab": ['13d36.7', '15d17.6', 2.49],
        "Menkar": ['314d13.0', '4d09.0', 2.5],
        "Menkent": ['148d05.6', '-36d26.6', 2.06],
        "Miaplacidus": ['221d38.4', '-69d46.9', 1.7],
        "Mirfak": ['308d37.4', '49d55.1', 1.82],
        "Nunki": ['75d56.6', '-26d16.4', 2.06],
        "Peacock": ['53d17.2', '-56d41.0', 1.91],
        "Polaris": ['316d41.3', '89d20.1', 2.01],
        "Pollux": ['243d25.2', '27d59.0', 1.15],
        "Procyon": ['244d57.5', '5d10.9', 0.34],
        "Rasalhague": ['96d05.2', '12d33.1', 2.1],
        "Regulus": ['207d41.4', '11d53.2', 1.35],
        "Rigel": ['281d10.1', '-8d11.3', 0.12],
        "Rigil Kentaurus": ['139d49.6', '-60d53.6', -0.01],
        "Sabik": ['102d10.9', '-15d44.4', 2.43],
        "Schedar": ['349d38.4', '56d37.7', 2.25],
        "Shaula": ['96d20.0', '-37d06.6', 1.62],
        "Sirius": ['258d31.7', '-16d44.3', -1.47],
        "Spica": ['158d29.5', '-11d14.5', 1.04],
        "Suhail": ['222d50.7', '-43d29.8', 2.23],
        "Vega": ['80d38.2', '38d48.1', 0.03],
        "Zubenelgenubi": ['137d03.7', '-16d06.3', 3.28]
    }
    return tempDictionary

def calculateGHA(currYear, observationDate, observationTime):
    referenceGHA = 100 + (42.6 / 60)
    declineGHA = 0 + (14.31667 / 60)
    dailyRotation = 0 + (59.0 / 60)
    numLeapYears = 0
    earthRotationalPeriod = 86164.1
    dateFormatting = "%Y-%m-%d %H:%M:%S"
    currentYearDate = str(currYear) + "-01-01 00:00:00" 
    observationComplete = str(observationDate) + " " + str(observationTime)
    beginCurrentYear = datetime.strptime(currentYearDate, dateFormatting)
    observationCurrent = datetime.strptime(observationComplete, dateFormatting)
    beginCurrentYearSeconds = time.mktime(beginCurrentYear.timetuple())
    observationCurrentSeconds = time.mktime(observationCurrent.timetuple())
    differenceInSeconds = observationCurrentSeconds - beginCurrentYearSeconds
    
    for y in range(2001, int(currYear)):
        if (y%4==0 and y%100!=0 or y%400==0):
            numLeapYears += 1
            
    cumulativeProgression = (int(currYear) - 2001) * -(declineGHA)
    leapProgression = dailyRotation * numLeapYears
    beginGHAAries = referenceGHA + cumulativeProgression + leapProgression
    observationRotation = differenceInSeconds / earthRotationalPeriod * 360
    observationRotation = observationRotation % 360
    currentGHAAries = beginGHAAries + observationRotation
    
    return currentGHAAries