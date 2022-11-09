#Simple class that allows you to send and receive messages over a serial port.

from machine import UART,Pin
from time import time_ns

class HC12:
    uart_id = 0
    baud_rate = 2400
    timeout = 1000 # milliseconds
    tx = 0
    rx = 1
    
    def __init__(self, uart_id:int, baud_rate:int=None, tx:int=None,rx:int=None):
        self.uart_id = uart_id
        if baud_rate: self.baud_rate = baud_rate
        if tx: self.tx = tx
        if rx: self.rx = rx

        # Initialise the UART serial port
        self.uart = UART(self.uart_id,self.baud_rate,tx = Pin(self.tx),rx = Pin(self.rx))

        # Initialise the UART serial port
        #self.uart.init()
            
    def send(self, message:str):
        print(f'sending message: {message}')
        message = message + '\n'
        self.uart.write(bytes(message,'utf-8'))
        
    def start(self):
        message = "successfully started.\n"
        print(message)
        self.send(message)

    def read(self)->str:
        start_time = time_ns()
        current_time = start_time
        new_line = False
        message = ""
        while (not new_line) or (current_time <= (start_time + self.timeout)):
            if (self.uart.any() > 0):
                try: message = message + self.uart.read().decode('utf-8')
                except: pass
                if '\n' in message:
                    new_line = True
                    message = message.strip('\n')
                    print(f'received message: {message}')
                    return message
        else:
            return None
        

