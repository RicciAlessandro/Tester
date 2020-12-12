import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p.name)

#ser = serial.Serial('/dev/ttyUSB0')  # open serial port
#print(ser.name)         # check which port was really used
#ser.write(b'hello')     # write a string
#ser.close()

nPort = int(input("inserisci la porta che vuoi aprire"))

ser = serial.Serial()
ser.baudrate = 9800
ser.port = 'COM%s' % (nPort) 
ser.timeout = 10
#ser
#Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
ser.open()
#ser.is_open
helloWord = bytes(0x11)
ser.write(helloWord)
data = ser.read()
print(data)
ser.close()
