import serial

serialPort = "COM5" 
baudRate = 9600  
ser = serial.Serial(serialPort, baudRate, timeout=0.5)
print("port=%s ，baudrate=%d" % (serialPort, baudRate))

while 1:
    str = ser.readline()
    Ta=str[4:5]
    Tb=str[5:6]
    Tc=str[6:7]
    Td=str[7:8]
    Te=str[8:9]
    Ha=str[10:11]
    Hb=str[11:12]
    Hc=str[12:13]
    Hd=str[13:14]
    He=str[14:15]
    
    print(Ta) 
    print(Tb)
    print(Tc)
    print(Td)
    print(Ha)
    print(Hb)
    print(Hc)
    print(Hd)
    print(He)
    
    ser.write(Ta)
    ser.write(Tb)
    ser.write(Tc)
    ser.write(Td)
    ser.write(Te)
    ser.write(Ha)
    ser.write(Hb)
    ser.write(Hc)
    ser.write(Hd)
    ser.write(He)
    '''
    Ta=str[4:6]
    Tb=str[6:7]
    Tc=str[7:9]
    Ha=str[10:12]
    Hb=str[12:13]
    Hc=str[13:15]
    print(Ta) 
    print(Tb)
    print(Tc)
    print(Ha)
    print(Hb)
    print(Hc)
    ser.write(Ta,Tb,Tc,Td,Te)
    '''


