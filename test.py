# Write dynamic and static data to a .csv (1 sample)
columns = 'Crash_ID,Crash_Datetime,Crash_Speed_Limit,Road_Algn_ID,Surf_Cond_ID,Wthr_Cond_ID,Light_Cond_ID,Crash_Sev_ID,Damaged_Property,Death_Cnt,Tot_Injry_Cnt,Prsn_Injry_Sev_ID,Prsn_Ejct_ID,Prsn_Airbag_ID,Rpt_Street_Name,Rpt_Sec_Hwy_Num,Crash_Time,risk_level\n'

data = '18039324,1/1/2021 10:50,65,3,'+ str(2) + ',' + str(3) + ',' + str(4) + ',' + '1,,0,0,5,0,2,IH 10 W,410,2,2\n'

with open('data.csv', 'w') as file:
    # Write content to the file
    file.write(columns)
    file.write(data)