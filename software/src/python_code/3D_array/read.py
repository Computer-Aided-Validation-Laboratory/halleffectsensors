'''script for simply reading and saving calibration data - processing comes after'''

import csv
from pathlib import Path
import time
import serial
import pandas as pd

def read_data(port: str, filename: str, samples: int = 400) -> None:
    '''
    method for reading data from the sensor array from the Arduino. uses the
    serial library to read in the data, opens a csv and stores the data in
    that csv.
    Args:
        port (str): the computer port that the sensor array is connected to
        filename (str): the name of the file that the data is stored under
        samples (int): how many data samples are read in
    Returns:
        None
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

if __name__ == "__main__":
    read_data(port = '/dev/ttyUSB0', filename = 'calib_1.csv', samples = 400)
