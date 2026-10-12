import json
from pathlib import Path
import pandas as pd
# so will have a json file coming in

path_json = Path(__file__).parent
output_json = path_json/'json.json'

with open(output_json, encoding='utf-8') as f:
    sensor_data = json.load(f)

data_path = Path(__file__).resolve().with_name('example.csv')
data = pd.read_csv(data_path)

number_of_sensors = 6
x = 0
i = 0

x_data = pd.DataFrame(dtype = float)
x_data['times_ms'] = data[data.columns[0]]
y_data = x_data.copy()
z_data = x_data.copy()

print(x_data)
print(y_data)
print(z_data)

print(sensor_data["sensors"][0]["index"][0])

print(sensor_data["sensors"][0]["index"])


while x < number_of_sensors:
    for sensor in sensor_data['sensors']:
        if i == sensor_data["index"][i]:
            if sensor_data['direction'] == 'x':
                x_data[x_data.columns[x+1]] = data[data.columns[i]]
                x+=1
            if sensor_data['direction'] == 'y':
                y_data[y_data.columns[x+1]] = data[data.columns[i]]
                x+=1
            if sensor_data['direction'] == 'z':
                z_data[z_data.columns[x+1]] = data[data.columns[i]]
                x+=1
        
            i+=1


# okay this isnt working, work this out on wednesday!




