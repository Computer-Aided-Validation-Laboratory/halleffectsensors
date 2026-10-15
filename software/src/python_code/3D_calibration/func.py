'''reads the data in from the Arduino'''
import json
import csv
from pathlib import Path
import time
import serial
import pandas as pd
import numpy as np

def read_data(port: str, filename: str, samples: int=400) -> None:
    '''
    docstring
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

def split_data(port: str, filename: str, samples: int, number: int) -> pd.DataFrame:
    '''ds'''

    path_json = Path(__file__).parent
    output_json = path_json/'json.json'

    with open(output_json, encoding = 'utf-8') as f:
        sensor_data = json.load(f)

    #total_input_df = read_data(port, filename, samples)
    data_path =  Path(__file__).resolve().with_name('example.csv')
    total_input_df = pd.read_csv(data_path)
    rows = total_input_df.shape[0]

    x_data = pd.DataFrame(np.zeros((rows, (int(number/3)+1))), dtype = float)
    x_data[x_data.columns[0]] = total_input_df[total_input_df.columns[0]]
    new_cols = ['time_ms']
    new_cols.extend([f'x_sensor_{i}' for i in range(1, int(number/3)+1)])
    x_data.columns = new_cols

    y_data = pd.DataFrame(np.zeros((rows, (int(number/3)+1))), dtype = float)
    y_data[y_data.columns[0]] = total_input_df[total_input_df.columns[0]]
    new_cols = ['time_ms']
    new_cols.extend([f'y_sensor_{i}' for i in range(1, int(number/3)+1)])
    y_data.columns = new_cols

    z_data = pd.DataFrame(np.zeros((rows, (int(number/3)+1))), dtype = float)
    z_data[z_data.columns[0]] = total_input_df[total_input_df.columns[0]]
    new_cols = ['time_ms']
    new_cols.extend([f'z_sensor_{i}' for i in range(1, int(number/3)+1)])
    z_data.columns = new_cols

    i = x = z = y = 0

    for sensor in sensor_data["sensors"]:
        i +=1
        if sensor["index"] == i:
            if sensor["direction"] == "x":
                x_data[x_data.columns[x+1]] = total_input_df[total_input_df.columns[i]]
                x+=1
            elif sensor["direction"] == "y":
                y_data[y_data.columns[y+1]] = total_input_df[total_input_df.columns[i]]
                y+=1
            elif sensor["direction"] == "z":
                z_data[z_data.columns[z+1]] = total_input_df[total_input_df.columns[i]]
                z+=1

    return x_data, y_data, z_data