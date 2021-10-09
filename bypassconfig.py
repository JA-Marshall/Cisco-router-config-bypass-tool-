import serial 
import time


class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)


def printserialdata():
    ser = serial.Serial('COM3', 9600)
    rl = ReadLine(ser)
    confreg = False
    inios = False
    input("\n\nPower cycle router and press enter immediatley to attempt password reset \n\n")
    while confreg == False:      
        output = str(rl.readline())
        print(output[12:-4])
        #print("...")
        ser.send_break(duration=0.2)
        if 'aborted' in output:
            print("\n\nChanging config register to bypass password...\n\n")
            time.sleep(2)
            ser.write("confreg 0x2142\r\n".encode())
            input("\n\n Config register changed. Power cycle and press enter to boot into router \n\n ")
            confreg = True
    print(output)

    while inios == False:
        output = str(rl.readline())
        print(output[12:-4])
        #print("...")
        if '--- System Configuration Dialog ---' in output:
            print("\n\n Bypassed password configuration complete, managed to booted into IOS \n\n ")
            inios = True


printserialdata() 
