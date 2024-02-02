# Ramin Mohammadi
    
def get_sense_hat_data(sense_hat):
    # Get sensor data
    temp = sense_hat.get_temperature() # celsius
    humidity = sense_hat.get_humidity()
    
    # Dew point formula
    dew_point = temp - ((100 - humidity)/5)
    
    return temp, humidity, dew_point

def get_light_sensor_data(light_sensor):
    # Read and calculate the light level in lux
    return light_sensor.lux

# Road Surface Condition, determined using temp and humidity
# pass sensor hat object
def get_surf_cond_id(sense_hat): 
    temp, humidity, dew_point = get_sense_hat_data(sense_hat)
    
    id = 1 # initialize
    # DRY
    if dew_point <= 55:
        id = 1
    # WET
    elif dew_point >= 65:
        id = 2
    # STANDING WATER? 
    # SLUSH?
    # SNOW, freezing with moisture
    elif temp <= 0 and humidity >= 70:
        id = 4
    # ICE, freezing
    elif temp <= 0:
        id = 3
        
    return id
    
# Weather Condition, determined using humidity, light (lux) and temp
# pass in sensor hat and light sensor objects
def get_wthr_cond_id(sense_hat, light_sensor):
    temp, humidity, dew_point = get_sense_hat_data(sense_hat)
    lux = get_light_sensor_data(light_sensor)
    
    id = 1
    # CLEAR
    if dew_point <= 55 and lux > 30000:
        id = 1
    # CLOUDY
    elif dew_point <= 65 and (10000 <= lux <= 30000):
        id = 2
    # RAIN
    elif temp > 0 and dew_point >= 65:
        id = 2
    # SLEET/HAIL?
    # SNOW
    elif temp <= 0 and humidity >= 70:
        id = 3
    # FOG
    elif (abs(dew_point - temp) < 2.5) or humidity == 100:
        id = 3
    # SEVERE CROSSWINDS?
    
    return id

# Light Condition, determined using light sensor lux value
def get_light_cond_id(light_sensor):
    lux = get_light_sensor_data(light_sensor)

    id = 1
    # DAYLIGHT
    if lux >= 10000:
        id = 1
    # DAWN (sunrise) / DUSK (sunset)
    elif 200 < lux < 10000:
        id = 1
    # DARK, LIGHTED
    elif 10 < lux <= 200:
        id = 3
    # DARK, NOT LIGHTED
    elif lux <= 10:
        id = 4
    # DARK UNKNOWN LIGHTING?
    
    return id