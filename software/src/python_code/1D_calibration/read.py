'''reads the data in from the Arduino'''

import csv
from pathlib import Path
import time
import serial
import pandas as pd


def read_data(port: str, filename: str, samples: int = 200) -> pd.DataFrame:
    '''
    Uses the serial library to get the data from the arduino, saves it as a csv file.
    Args:
        port (str): computer port that the arduino is connected to
        filename (str): filename that the data is saved under (csv)
        samples (int): how many samples (timestamps) are read
    Retuns:
        df (pd.DataFrame): the dataframe that the arduino data is stored in
    '''

    ser = serial.Serial(port, 9600)
    ser.reset_input_buffer()
    time.sleep(2)
    script_dir = Path(__file__).parent
    csv_file = script_dir / filename

    with open(csv_file, 'w', newline = '', encoding = 'utf-8') as csvfile:
        writer = csv.writer(csvfile)

        while True:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()

            if "time_ms" in raw:
                header = raw
                break

        header = header[header.find("time_ms"):]
        header = header.replace('\x00', '').strip()
        writer.writerow(header.split(","))

        samples_taken = 0

        while samples_taken < samples:
            line = ser.readline().decode().strip()
            if line:
                values = line.split(',')
                writer.writerow(values)
                print(values)

                samples_taken += 1

    ser.close()

    df = pd.read_csv(csv_file, skipinitialspace=True)
    return df
