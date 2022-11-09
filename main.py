import serial
import time
import json


def ciclo():
    #num = 1
    while True:
        if(ser.isOpen()):
            try:
                dt = ser.readline()
                Dt_s = dt.decode('UTF-8')
                dt_list = Dt_s[:-1].split(",")
            except:
                dt_list = ['24.1', '38.0', '1007', '1.04', '-0.06', '-0.06', '-2', '6', '0']
            
            
            if len(dt_list) == 13:
                dt_json = json.dumps(dt_list[:-4])
                with open('./data.json','w') as outfile:
                    outfile.write(dt_json)

                #gps_json = json.dumps(dt_list[9:])
                try:
                    lat = int(dt_list[-4][:2])
                    lat_min = int(dt_list[-4][2:4])
                    lat_sec = round(float(dt_list[-4][4:])*60,4)
                    lat_dir = dt_list[-3]

                    lon = int(dt_list[-2][:3])
                    lon_min = int(dt_list[-2][3:5])
                    lon_sec = round(float(dt_list[-2][5:])*60,4)
                    lon_dir = dt_list[-1]
                except: pass

                gps_list = [lat,lat_min,lat_sec,lat_dir,lon,lon_min,lon_sec,lon_dir]
                gps_json = json.dumps(gps_list)
                with open('./gps.json','w') as outfile:
                    outfile.write(gps_json)
                    #41°24'12.2"N 2°10'26.5"E
                    # If the GPS Receiver reports a Latitude of 4717.112671 North and Longitude of 00833.914843 East, this is
                    # Latitude 47 Degrees, 17 Minutes, 6.76026 Seconds
                    # Longitude 8 Degrees, 33 Minutes, 54.89058 Seconds

                print(dt_list)
            else: pass
            
            
            f = open('obj.json')
            light = json.load(f)
            num = int(light[-1:])

            ser.write(bytes(str(num)+'\r\n','utf-8'))
            #print('enviando: '+str(num)+'\r\n')
            time.sleep(2)
            
            
        else:
            pass

with serial.Serial('COM5',2400,timeout=1) as ser:
    try:
        ser.open()
        print('conectado')
        ciclo()
    except:
        if(ser.isOpen()):
            print('conectado')
            ciclo()
        else:
            print('sin conexion')


