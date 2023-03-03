import asyncio
import serial_asyncio
import queue
import datetime
#import re
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

port = 'COM10'
filename = '2023-03-02_co2_test.csv'

incoming_serial_queue = queue.Queue()

def parse_sable(b):
    str_rn = b.decode()
    str = str_rn.rstrip()
    str_c = str.removeprefix('!!!:ca2a:4,')
    str_d = str_c.split(',')
    dat = [float(str) for str in str_d]
    return dat

async def read_serial(port):
    print("do serial")
    reader, writer = await serial_asyncio.open_serial_connection(url = port, baudrate = 9600)
    while True:
        raw = await reader.readline()
        data = parse_sable(raw)
        ts = datetime.datetime.now()
        #print("put: " + ts + " " + data)
        incoming_serial_queue.put((ts, data))

async def main():
    print("main")
    with open(filename, 'a', buffering = 1) as the_file:
        while True:
            if not incoming_serial_queue.empty():
                data = incoming_serial_queue.get()
                data_str = ','.join(map(str,data[1]))
                print("get: " + str(data[0]) + ',' + data_str)
                the_file.write(str(data[0]) + ',' + data_str + '\n')
            await asyncio.sleep(0.01)

async def start():
    print("start")
    await asyncio.gather(
        read_serial(port),
        main(),
    )

asyncio.run(start())
