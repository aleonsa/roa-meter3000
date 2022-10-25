import serial
import time
import json


def ciclo():
    #num = 1
    while True:
        if(ser.isOpen()):
            #if num == 0: num = 1
            #else: num = 0
            dt = ser.readline()
            Dt_s = dt.decode('UTF-8')
            dt_list = Dt_s[:-3].split(",")
            dt_json = json.dumps(dt_list)
            with open('./data.json','w') as outfile:
                outfile.write(dt_json)
            print(dt_list)
            f = open('obj.json')
            light = json.load(f)
            num = int(light[-1:])

            ser.write(bytes(str(num)+'\r\n','utf-8'))
            time.sleep(2)
            
            
        else:
            ser.write(bytes(str(num)+'\r\n','utf-8'))
            

with serial.Serial('COM8',9600,timeout=1) as ser:
    try:
        ser.Open()
        print('conectado')
        ciclo()
    except:
        if(ser.isOpen()):
            print('conectado')
            ciclo()
        else:
            print('sin conexion')


