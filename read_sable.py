# read and parse sable co2 serial

import serial
import time
import csv

ser = serial.Serial('COM4', 9600)
ser.flushInput()

def parse_sable(b):
    str_rn = b.decode()
    str = str_rn.rstrip()
    str_c = str.removeprefix('!!!:ca2a:4,')
    str_d = str_c.split(',')
    dat = [float(str) for str in str_d]
    return dat

def sable_acquire():
    ser.flushInput()
    while True:
        try:
            ser_bytes = ser.readline()
            decoded_bytes = parse_sable(ser_bytes)
            print(decoded_bytes)
            with open("test_data.csv","a") as f:
                writer = csv.writer(f,delimiter=",")
                writer.writerow([time.time()] + decoded_bytes)
        except:
            print("Keyboard Interrupt")
            break

if __name__ == "__main__":
    sable_acquire()
