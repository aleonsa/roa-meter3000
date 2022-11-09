import utime
from machine import I2C, Pin, SoftI2C, UART
from pico_i2c_lcd import I2cLcd
from dht import DHT11, InvalidChecksum
from imu import MPU6050
import time
from bmp180 import BMP180
import sys
import _thread
import hc12

#GPS
gps = UART(0,9600,tx=Pin(12),rx=Pin(13))
buff = bytearray(255)
#HC12 init
hc12 = hc12.HC12(uart_id=1, baud_rate=2400, tx=8, rx=9)
#hc12.start()

#Address of I2C and size of LCD
i2c = I2C(id=0, scl=machine.Pin(17),sda=machine.Pin(16), freq=400000)
addr_lcd = i2c.scan()[0]
I2C_ADDR = addr_lcd
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

#BMP180 sensor, pressure
bus =  SoftI2C(scl=Pin(7), sda=Pin(6), freq=200000,timeout=50000)   # on esp8266
bmp180 = BMP180(bus)
bmp180.oversample_sett = 3
baseline = bmp180.pressure/100
ALTURA = 2280

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()

lcd.putstr('Cargando...')

##led
led = Pin(5,Pin.PULL_DOWN)

#DHT11 sensor, temperature and humidity
#DHT11
pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
dht = DHT11(pin)

bus_mpu = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
imu = MPU6050(bus_mpu)
x = ''
def Lectura():
    while True:
        global x
        data=hc12.read()
        x = data
        utime.sleep(1)
        
_thread.start_new_thread(Lectura,())

degree_sym = bytearray([0x0E,0x0A,0x0E,0x00,0x00,0x00,0x00,0x00])
lcd.custom_char(0,degree_sym)

while True:
    
    utime.sleep(1.5)
    
    try: #try to read all data
        if (gps.any() > 0):
            data = gps.readline()
            buff = str(data)[:-5]
            parts = buff.split(',')
            if "b'$GPGLL" in parts[0] and len(parts)==8:
        # $GPGLL, lat, lat_dir, lon, lon_dir, utc, data_status, mode_ind*xx
            #print("data is: " + buff)
                gps_data = str(str(parts[1])+','+str(parts[2])+','+str(parts[3])+','+str(parts[4]))
            else:
                gps_data = '1919.71726,N,09910.65431,W'
                #ultima data registrada en ed. Q facultad de ing. UNAM
        
        t  = (dht.temperature)
        h = (dht.humidity)
        p = round(bmp180.pressure/100 * 1.333) - 31
        #MPU6050, giroscope
        # Following print shows original data get from libary. You can uncomment to see raw data
        #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')
        
        # Following rows round values get for a more pretty print:
        ax=round(imu.accel.x,2)
        ay=round(imu.accel.y,2)
        az=round(imu.accel.z,2)
        gx=round(imu.gyro.x)
        gy=round(imu.gyro.y)
        gz=round(imu.gyro.z)
        #print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,end="\r")
        #print('\n')
        
        # Following sleep statement makes values enough stable to be seen and
        # read by a human from shell
    except:
        pass
      
    send = (str(t)+","+str(h)+","+str(p)+","+str(ax)+","+str(ay)+","+str(az)+","+str(gx)+","+str(gy)+","+str(gz)+","+gps_data)
    #sys.stdout.write(send+"\r\n")
    hc12.send(send)
    
    lcd.clear()
    
    lcd.putstr("T:{}".format(round(t))+chr(0)+'C ')
    lcd.putstr("H:{}%".format(round(h)))
    lcd.move_to(0, 1)
    lcd.putstr("P:{} hPa".format(round(p)))
    try: #try to read from serial port if there is an instruction for light bulb
        a=int(x[0])
        if a == 1:
            led.value(0)
            #sys.stdout.write('foco encendido \r\n')
        else:
            led.value(1)
            #sys.stdout.write('foco apagado \r\n')
    except: pass
    x = ''
    