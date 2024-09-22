from sense_hat import SenseHat
import board
import busio
import adafruit_tsl2591
import serial
import quantize_sensor_values
import torch
from get_prediction_labels import get_prediction_labels

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

'''
# Write dynamic and static data to a .csv (1 sample)
columns = 'Crash_ID,Crash_Datetime,Crash_Speed_Limit,Road_Algn_ID,Surf_Cond_ID,Wthr_Cond_ID,Light_Cond_ID,Crash_Sev_ID,Damaged_Property,Death_Cnt,Tot_Injry_Cnt,Prsn_Injry_Sev_ID,Prsn_Ejct_ID,Prsn_Airbag_ID,Rpt_Street_Name,Rpt_Sec_Hwy_Num,Crash_Time,risk_level\n'

data = '18039324,1/1/2021 10:50,65,3,'+ str(surf_cond_id) + ',' + str(wthr_cond_id) + ',' + str(light_cond_id) + ',' + '1,,0,0,5,0,2,IH 10 W,410,2,2\n'

with open('data.csv', 'w') as file:
    # Write content to the file
    file.write(columns)
    file.write(data)
'''

# ------ Predict injury type using pretrained AI model with a SINGLE sample -------
#(example seems to be in Sahidul's evaluate() function)

# load pretrained model
net = torch.load('Safety_net_0.pkl')
print(net)

# tell pytorch whether to use CPU or GPU. Use CPU
device = 'cpu'
net = net.float().to(device)

# put model in eval mode (there are different modes: train, eval (used to test model), etc...)
net.eval()

'''
Input data should be a TENSOR of shape: (#samples x 1 x 62 features x 1)
representing: [row, channel, features_X, featureY]
Here there is 1 channel and featureY is 1 because this is 1D data

62 features are the following:

['Crash_ID', 'Crash_Fatal_Fl', 'Schl_Bus_Fl', 'Rr_Relat_Fl', 'Medical_Advisory_Fl', 'Active_School_Zone_Fl',
'Rpt_Outside_City_Limit_Fl','Thousand_Damage_Fl', 'Rpt_Latitude', 'Rpt_Longitude',
'Private_Dr_Fl', 'Toll_Road_Fl', 'Crash_Speed_Limit', 'Road_Constr_Zone_Fl', 'Road_Constr_Zone_Wrkr_Fl',
'Wthr_Cond_ID', 'Light_Cond_ID', 'Road_Type_ID', 'Road_Algn_ID', 'Surf_Cond_ID', 'Traffic_Cntl_ID',
'Cnty_ID', 'City_ID', 'Latitude', 'Longitude', 'Txdot_Rptable_Fl', 'Onsys_Fl', 'Rural_Fl', 'Pop_Group_ID',
'Located_Fl', 'Hp_Shldr_Left', 'Hp_Shldr_Right', 'Hp_Median_Width', 'Nbr_Of_Lane', 'Row_Width_Usual', 'Roadbed_Width',
'Surf_Width', 'Surf_Type_ID', 'Curb_Type_Right_ID', 'Shldr_Type_Left_ID', 'Shldr_Width_Left', 'Shldr_Use_Left_ID',
'Shldr_Type_Right_ID', 'Shldr_Width_Right', 'Shldr_Use_Right_ID', 'Median_Type_ID', 'Median_Width', 'Rural_Urban_Type_ID',
'Func_Sys_ID', 'Adt_Curnt_Amt', 'Adt_Curnt_Year', 'Adt_Adj_Curnt_Amt', 'Pct_Single_Trk_Adt', 'Pct_Combo_Trk_Adt',
'Trk_Aadt_Pct', 'Sus_Serious_Injry_Cnt', 'Nonincap_Injry_Cnt', 'Poss_Injry_Cnt', 'Non_Injry_Cnt', 'Unkn_Injry_Cnt',
'Tot_Injry_Cnt', 'Death_Cnt']
'''
# 1 sample from dataset
input_data = [[[[16559000.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [0.0], [30.0], [0.0], [0.0], [11.0], [4.0], [0.0], [1.0], [1.0], [20.0], [254.0], [27.544], [-99.511], [1.0], [0.0], [0.0], [8.0], [1.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0]]]]
# print(input_data[0][0][7][0])

# wthr_cond_id is the 16th value/feature
input_data[0][0][15][0] = wthr_cond_id
# light_cond_id is the 17th value/feature
input_data[0][0][16][0] = light_cond_id
# surf_cond_id is the 20th value/feature
input_data[0][0][19][0] = surf_cond_id

input_data = torch.tensor(input_data)

# pass input data into model and receive output prediction(s)
outputs_test = net(input_data)
print("Output: ", outputs_test)

_, predicted_test_id = torch.max(outputs_test.data, 1)

prediction = get_prediction_labels(predicted_test_id)

# The output is between 0 to 5, representing unknown, serious, minor, possible, fatal, no-injury. 
print("Predicted: ", predicted_test_id, ", ", prediction)

#---------------------------------------------------------------

# MAKE SURE transmitter is plugged into bottom right usb and use /dev/ttyUSB0
ser = serial.Serial("/dev/ttyUSB0", 115200)

# ---- Send message to receiver ---- #
send_mess = ""
temp, humidity, dew_point = quantize_sensor_values.get_sense_hat_data(sense_hat)
lux = quantize_sensor_values.get_light_sensor_data(light_sensor)
# Humidity
send_mess += "H: {0}\n".format(round(humidity,2))
# Light (lux value)
send_mess += "L: {0}\n".format(round(lux,2))
# Prediction of the likeliness of the type of injury if a crash occurs
send_mess += prediction + "\n"
#send_mess += "R: High" # manually change to Low, Medium, High for now
# Write message to Serial port.
ser.write(send_mess.encode())
#------------------------------------#


