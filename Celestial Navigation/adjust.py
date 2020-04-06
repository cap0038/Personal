'''
    Created on February 17th, 2019

    @author:    Cait Potridge
'''
import math

def adjust(values=None):
    if (not('observation' in values) or (values['observation'] == '')):
        values['error'] = 'mandatory information is missing.'
        return values
    if ((not('height' in values)) or (values['height'] == '')):
        height = 0
    else:
        height = values['height']
    if ((not('temperature' in values)) or (values['temperature'] == '')):
        temperature = 72
    else:
        temperature = values['temperature']
    if ((not('pressure' in values)) or (values['pressure'] == '')):
        pressure = 1010
    else:
        pressure = values['pressure']
    if ((not('horizon' in values)) or (values['horizon'] == '')):
        horizon = 'natural'
    else:
        horizon = values['horizon']
    
    observation = values['observation']
    placeOfD = observation.find('d')
    if (placeOfD != -1):    
        x = observation[:placeOfD]
        y = observation[(placeOfD + 1):]
        try:
            x = int(x)
            y = float(y)
        except:
            values['error'] = 'observation is invalid'
            return values
    else:    
        values['error'] = 'observation is invalid'
        return values
    
    if ((x < 1) or (x >= 90)):
        values['error'] = 'observation is invalid'
        return values
    
    if ((y < 0.0) or (y > 60.0)):
        values['error'] = 'observation is invalid'
        return values
    
    if (height != 0):
        try:
            height = int(height)
        except:
            values['error'] = 'height is invalid'
            return values
        
    if (height < 0):
        values['error'] = 'height is invalid'
        return values
    
    if (temperature != 72):
        try:         
            temperature = int(temperature)
        except:
            values['error'] = 'temperature is invalid'
            return values
    
    if ((temperature < -20) or (temperature >= 120)):
        values['error'] = 'temperature is invalid'
        return values
    
    if(pressure != 1010):
        try: 
            pressure = int(pressure)
        except:
            values['error'] = 'pressure is invalid'
            return values
    
    if ((pressure < 100) or (pressure > 1100)):
        values['error'] = 'pressure is invalid'
        return values
    
    if(horizon != 'natural'):
        try:    
            horizon = horizon.lower()
            horizon = horizon.strip()
            if ((horizon != 'natural') and (horizon != 'artificial')):
                values['error'] = 'horizon is invalid'
                return values
        except:
            values['error'] = 'horizon is invalid'
            return values
    
    # Actual Calculations
    if (horizon == 'natural'):
        dip = (-0.97 * math.sqrt(height)) / 60
    else:
        dip = 0
    
    celsiusTemperature = (temperature - 32) / 1.8
    observationCalculated = x + (y/60)
    
    refraction=(-0.00452*pressure) / (273 + celsiusTemperature)/math.tan(math.radians(observationCalculated))
    
    altitude = observationCalculated + dip + refraction
    altitudeX = int(altitude)
    altitudeY = altitude - altitudeX
    altitudeY = round(altitudeY * 60, 1)
    
    finalAltitude = str(altitudeX) + 'd' + str(altitudeY)
    values['altitude'] = finalAltitude
    
    return values