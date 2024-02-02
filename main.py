from sense_hat import SenseHat
import board
import busio
import adafruit_tsl2591
import serial
import quantize_sensor_values
import torch

# --- Sensor Hat -------------
sense_hat = SenseHat()
#-----------------------------

# --- Sending Message, Receiver to Transmitter --- #
# MAKE SURE transmitter is plugged into bottom right usb and use /dev/ttyUSB0
ser = serial.Serial("/dev/ttyUSB0", 115200) 
# ------------------------------------------------- #

# --- Light Sensor -------------
# Initialize the I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Initialize the sensor.
light_sensor = adafruit_tsl2591.TSL2591(i2c)
#-------------------------------

# get dynamic input values (Surface, weather, and light conditions)
surf_cond_id = quantize_sensor_values.get_surf_cond_id(sense_hat)
wthr_cond_id = quantize_sensor_values.get_wthr_cond_id(sense_hat, light_sensor)
light_cond_id = quantize_sensor_values.get_light_cond_id(light_sensor)

print('Surface Condition ID: ', surf_cond_id)
print('Weather Condition ID: ', wthr_cond_id)
print('Light Condtion ID: ', light_cond_id)

# static data (1 sample)
# Crash_Id = '18039324'
# Crash_Datetime = '1/1/2021 10:50'
# Crash_Speed_Limit = '65'
# Road_Algn_ID = '3'
# # surf_cond_id, 
# # wthr_cond_id, 
# # light_cond_id,
# Crash_Sev_ID = '1'
# Damaged_Property = ''
# Death_Cnt = '0'
# Tot_Injry_Cnt = '0'
# Prsn_Injry_Sev_ID = '5'
# Prsn_Ejct_ID = '0'
# Prsn_Airbag_ID = '2'
# Rpt_Street_Name = 'IH 10 W'
# Rpt_Sec_Hwy_Num = '410'
# Crash_Time = '2'
# risk_level = '2'

# Write dynamic and static data to a .csv (1 sample)
columns = 'Crash_ID,Crash_Datetime,Crash_Speed_Limit,Road_Algn_ID,Surf_Cond_ID,Wthr_Cond_ID,Light_Cond_ID,Crash_Sev_ID,Damaged_Property,Death_Cnt,Tot_Injry_Cnt,Prsn_Injry_Sev_ID,Prsn_Ejct_ID,Prsn_Airbag_ID,Rpt_Street_Name,Rpt_Sec_Hwy_Num,Crash_Time,risk_level\n'

data = '18039324,1/1/2021 10:50,65,3,'+ str(surf_cond_id) + ',' + str(wthr_cond_id) + ',' + str(light_cond_id) + ',' + '1,,0,0,5,0,2,IH 10 W,410,2,2\n'

with open('data.csv', 'w') as file:
    # Write content to the file
    file.write(columns)
    file.write(data)

# Predict Risk using pretrained AI model with a SINGLE sample
# (example seems to be in Sahidul's evaluate() function)
device = 'cpu'
net = torch.load('saved_models/Safety_net_0.pkl')
net = net.float().to(device)
net.eval() # -> eval method from parent of model class nn.Module?
outputs_test = net(data)