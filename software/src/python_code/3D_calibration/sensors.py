# this code only works for x,y,z in that order formatted sensors (need to use the config file to order them properly)
# can test this using 6 sensors first. This method only works because i know the order of directions that the data is in,
# which won't always be the same, so need the config file to specify what order the data is coming in as

'''code kind of ish works - needs to be fixed but not completely hopeless'''

# imports
from pathlib import Path
from csv import writer
import numpy as np
import pandas as pd
from read import read_data

class Nulls:
    '''
    doc
    '''
    def __init__(self, number: int, port: str, vcc: float, vcc_un: float, filename: str, bits: int, samples: int = 400):
        self.number = number
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.filename = filename
        self.bits = ((2**bits)-1)
        self.samples = samples

        self.data = None
        self.nulls = None
        self.stds = None
        self.uncertainties = None
        self.null_frame = None
        self.std_frame = None



        # so we will say that this data looks like this: (except will be for 12 sensors)
        # time/ms |  sensor 1  |  sensor 2  |  sensor 3  | 
        # 50      |  512       |  513       |  511       |    
        # 100     |  513       |  514       |  512       |
        # 150     |  514       |  511       |  510       |
        # 200     |  511       |  509       |  512       |
        # ------------------------------------------------
        #
        # so we will say that A0 is sensor 1, in the x direction, A2 is sensor 2 in the y direction,
        # A2 sensor 3 in the z direction so they will have a different field to calibrate against
        # but calculating the null voltage should be the same
    
        self.find_parameters()


    def find_parameters(self) -> None:
        '''
        docstring
        '''
        self.data = read_data(self.port, self.filename, self.samples)

        self.nulls = np.empty(self.number)
        self.stds = np.empty(self.number)

        for i in range(self.number):
            mean_value = self.data[self.data.columns[i+1]].mean()
            self.nulls[i] = mean_value * self.vcc / self.bits
            self.stds[i] = (self.data[self.data.columns[i+1]]).std(ddof=1)

        self.uncertainty()

    def uncertainty(self) -> None:
        '''ds'''

        self.uncertainties = np.empty(self.number)
        count_uncertainty = 0.5
        vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2

        for i in range(self.number):
            mean_reading = (self.data[self.data.columns[i+1]]).mean()
            uncertainty_in_reading  = ((np.sqrt((count_uncertainty)**2 + (self.stds[i])**2))/mean_reading)**2
            rooted = np.sqrt(uncertainty_in_reading + vcc_uncertainty)
            self.uncertainties[i] = (rooted*self.nulls[i])

        self.save_values()

    def save_values(self) -> None:
        '''ds'''
        self.null_frame = pd.DataFrame(np.zeros((2, self.number)), dtype = float)
        self.std_frame = pd.DataFrame(np.zeros((1, self.number)), dtype = float)

        self.null_frame.iloc[0] = self.nulls
        self.null_frame.iloc[1] = self.uncertainties
        self.std_frame.iloc[0] = self.stds

        file_dir = Path(__file__).parent
        output_file_nulls = file_dir / 'nulls.csv'
        output_file_stds = file_dir / 'stds.csv'

        self.null_frame.to_csv(output_file_nulls, index = False)
        self.std_frame.to_csv(output_file_stds, index = False)


class Calib:
    '''ds'''

    def __init__(self, number: int, port: str, vcc: float, vcc_uncertainty: float, filename: str, bits: int, samples: int=400):
        self.number = number # must be divisible by 3
        self.port = port
        self.vcc = vcc
        self.vcc_uncertainty = vcc_uncertainty
        self.filename = filename
        self.bits = ((2**bits)-1)
        self.samples = samples

        self.nulls = None
        self.data = None
        self.data2 = None
        self.stds = None
        self.nulls_uncertainties = None
        self.sensitivity_frame = None
        self.uncertainty = None
        self.data = None

        self.get_nulls()

    def get_nulls(self):
        '''ds'''
        self.nulls = np.empty(self.number)
        self.nulls_uncertainties = np.empty(self.number)
        self.stds = np.empty(self.number)

        path_nulls = Path(__file__).resolve().with_name('nulls.csv')
        parameters_df = pd.read_csv(path_nulls)

        path_stds = Path(__file__).resolve().with_name('stds.csv')
        stds_df = pd.read_csv(path_stds)

        self.nulls = parameters_df.iloc[0].to_numpy()
        self.nulls_uncertainties = parameters_df.iloc[1].to_numpy()
        self.stds = stds_df.iloc[0].to_numpy()

        self.perform_calibration(field = [34, 56, 36], field_uncertainty = 0.05)

    def perform_calibration(self, field: np.array, field_uncertainty: float=0.05) -> None:
        '''
        ds
        '''
        sensor_uncertainty = 0.5
        self.data = read_data(self.port, self.filename, self.samples)

        self.data2 = self.data.copy()

        sensitivities = np.empty(self.number)
        uncertainty = np.empty(self.number)
        self.sensitivity_frame = pd.DataFrame(np.zeros((6, int(self.number/3))))

        vcc_uncertainty = (self.vcc_uncertainty/self.vcc)**2

        x=0
        while x < 3: # when x=0, calibrates the x sensors, when x=1, calibrates the y sensors and when x=2,
            # calibrates the z sensors
            for i in range((int(self.number/3)-1)):
                self.data[self.data.columns[(3*i)+x+1]] = self.data[self.data.columns[(3*i)+x+1]] * self.vcc / self.bits
                self.data[self.data.columns[(3*i)+x+1]] -= self.nulls[(3*i)+x]
                sensitivities[(3*i)+x] = (np.mean((self.data[self.data.columns[(3*i)+x+1]]))/field[x])*1000

                average_count = np.mean(self.data2[self.data2.columns[(3*i)+x+1]])
                count_uncertainty = ((np.sqrt(((sensor_uncertainty)**2)+(self.stds[(3*i)+x])**2))/average_count)**2
                average_voltage = np.mean((self.data2[self.data2.columns[(3*i)+x+1]]*self.vcc / self.bits))
                uncertainty_in_voltage = average_voltage*(np.sqrt(count_uncertainty+vcc_uncertainty))
                uncertainty_in_voltage_nulls = (np.sqrt(((uncertainty_in_voltage)**2)+((self.nulls_uncertainties[(3*i)+x])**2)))
                self.data2[self.data2.columns[(3*i)+1+x]] = self.data2[self.data2.columns[(3*i)+1+x]]-self.nulls[(3*i)+x]
                uncertainty_in_null_total = ((uncertainty_in_voltage_nulls)/np.mean(self.data2[self.data2.columns[(3*i)+x+1]]))**2
                uncertainty_in_field_total = (field_uncertainty/field[x])**2
                uncertainty[(3*i)+x] = (np.sqrt(uncertainty_in_null_total+uncertainty_in_field_total))*sensitivities[(3*i)+x]

            print(self.sensitivity_frame.shape)
            print(self.sensitivity_frame)
            print(sensitivities)
            print(uncertainty)
   
            # these are being saved wrong i think
            self.sensitivity_frame.iloc[(2*x)] = sensitivities[x], sensitivities[x+3]
            self.sensitivity_frame.iloc[(2*x)+1] = uncertainty[x], uncertainty[x+3]
            x+=1

            print(self.sensitivity_frame)
            #then to extract this data, will need to know how many calibration fields are gonna be used
            # need to save these to csvs inside this loop

        self.save_sens()

    def save_sens(self) -> None:
        '''ds'''

        path = Path(__file__).parent
        output_x = path/'x_sens.csv'
        output_y = path/'y_sens.csv'
        output_z = path/'z_sens.csv'
        output_un_x = path/'x_sens_un.csv'
        output_un_y = path/'y_sens_un.csv'
        output_un_z = path/'z_sens_un.csv'

        sens_x = self.sensitivity_frame.iloc[0]
        sens_y = self.sensitivity_frame.iloc[2]
        sens_z = self.sensitivity_frame.iloc[4]

        sens_un_x = self.sensitivity_frame.iloc[1]
        sens_un_y = self.sensitivity_frame.iloc[3]
        sens_un_z = self.sensitivity_frame.iloc[5]

        with open(output_x, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_x)
        with open(output_y, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_y)
        with open(output_z, 'a', encoding = 'utf-8', newline = '')as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_z)
        with open(output_un_x, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_un_x)
        with open(output_un_y, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_un_y)
        with open(output_un_z, 'a', encoding = 'utf-8', newline = '') as f:
            writer_obj = writer(f)
            writer_obj.writerow(sens_un_z)

        # so will have a separate csv file now for each sensitivity direction and
        # each uncertainty in sensitivity direction.
        # every time this code runs it will append to the csv
        # then when these are wanting to be used in the actual data conversion can 
        # take an average of each column in each csv

class Convert:
    '''ds'''
    def __init__(self, port: str, filename: str, number: int, vcc: float,
                vcc_un: float, bits: int, samples: int = 200):
        self.port = port
        self.filename = filename
        self.number = number
        self.vcc = vcc
        self.vcc_uncertainty = vcc_un
        self.bits = (2**bits)-1
        self.samples = samples

        self.data = None
        self.sensitivities = None
        self.uncertainty_sensitivity = None
        self.nulls = None
        self.nulls_uncertainty = None
        self.stds = None

        self.voltage_uncertainty = None
        self.field_uncertainty = None

        self.data_x = None
        self.data_y = None
        self.data_z = None

        self.field_uncertainty_x = None
        self.field_uncertainty_y = None
        self.field_uncertainty_z = None

        self.get_params()

    def get_params(self) -> None:
        '''
        ds
        '''

        sensitivity_x_path = Path(__file__).resolve().with_name('x_sens.csv')
        sensitivity_y_path = Path(__file__).resolve().with_name('y_sens.csv')
        sensitivity_z_path = Path(__file__).resolve().with_name('z_sens.csv')

        sensitivity_uncertainty_x_path = Path(__file__).resolve().with_name('x_sens_un.csv')
        sensitivity_uncertainty_y_path = Path(__file__).resolve().with_name('y_sens_un.csv')
        sensitivity_uncertainty_z_path = Path(__file__).resolve().with_name('z_sens_un.csv')

        sensitivity_x_frame = pd.read_csv(sensitivity_x_path)
        sensitivity_y_frame = pd.read_csv(sensitivity_y_path)
        sensitivity_z_frame = pd.read_csv(sensitivity_z_path)

        sensitivity_un_x_frame = pd.read_csv(sensitivity_uncertainty_x_path)
        sensitivity_un_y_frame = pd.read_csv(sensitivity_uncertainty_y_path)
        sensitivity_un_z_frame = pd.read_csv(sensitivity_uncertainty_z_path)

        sens_x = np.empty(int(self.number/3))
        sens_y = np.empty(int(self.number/3))
        sens_z = np.empty(int(self.number/3))

        sens_un_x = np.empty(int(self.number/3))
        sens_un_y = np.empty(int(self.number/3))
        sens_un_z = np.empty(int(self.number/3))

        for i in range((int(self.number/3)) - 1):
            sens_x[i] = np.mean(sensitivity_x_frame[sensitivity_x_frame.columns[i]])
            sens_y[i] = np.mean(sensitivity_y_frame[sensitivity_y_frame.columns[i]])
            sens_z[i] = np.mean(sensitivity_z_frame[sensitivity_z_frame.columns[i]])
            sens_un_x[i] = np.mean(sensitivity_un_x_frame[sensitivity_un_x_frame.columns[i]])
            sens_un_y[i] = np.mean(sensitivity_un_y_frame[sensitivity_un_y_frame.columns[i]])
            sens_un_z[i] = np.mean(sensitivity_un_z_frame[sensitivity_un_z_frame.columns[i]])

        sensitivity = np.empty(self.number)
        uncertainty_sensitivity = np.empty(self.number)

        for i in range(self.number):
            if i%3 == 0: # x sensor
                sensitivity[i] = sens_x[i/3]
                uncertainty_sensitivity[i] = sens_un_x[i/3]
            elif i%3 == 1: # y sensor
                sensitivity[i] = sens_y[(i-1)/3]
                uncertainty_sensitivity[i] = sens_un_y[(i-1)/3]
            elif i%3 == 2: # z sensor
                sensitivity[i] = sens_z[(i-2)/3]
                uncertainty_sensitivity[i] = sens_un_z[(i-2)/3]

        self.sensitivities = sensitivity
        self.uncertainty_sensitivity = uncertainty_sensitivity
        
        self.nulls = np.empty(self.number)
        self.nulls_uncertainty = np.empty(self.number)
        self.stds = np.empty(self.number)

        nulls_path = Path(__file__).resolve().with_name('nulls.csv')
        stds_path = Path(__file__).resolve().with_name('stds.csv')
        nulls_and_uncertainties = pd.read_csv(nulls_path)
        self.nulls = nulls_and_uncertainties.iloc[0].to_numpy()
        self.nulls_uncertainty= nulls_and_uncertainties.iloc[1].to_numpy()
        stds_df = pd.read_csv(stds_path)
        self.stds = stds_df.iloc[0].to_numpy()

        # okay now i think i have all of them! hopefully all still in the same order...

        self.data = read_data(self.port, self.filename, self.samples)

        self.into_voltage()

    def into_voltage(self) -> None:
        '''ds'''

        self.voltage_uncertainty = np.empty(self.number)

        for i in range(self.number):
            sensor_uncertainty = np.sqrt(0.5+self.stds[i]) # need to check this saves as like a row instead of a column
            average_reading = np.mean(self.data[self.data.columns[i+1]])

            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] * self.vcc / self.bits

            average_voltage = np.mean(self.data[self.data.columns[i+1]])
            count_uncertainty = sensor_uncertainty/average_reading
            vcc_uncertainty = self.vcc_uncertainty/self.vcc
            voltage_uncertainty_without_nulls = average_voltage * (np.sqrt((count_uncertainty)**2 + (vcc_uncertainty)**2))

            self.data[self.data.columns[i+1]] = self.data[self.data.columns[i+1]] - self.nulls[i]

            self.voltage_uncertainty[i] = np.sqrt((self.nulls_uncertainty[i])**2+(voltage_uncertainty_without_nulls)**2)

        self.field_strengths()

    def field_strengths(self) -> None:
        '''ds'''
        self.field_uncertainty = np.empty(self.number)

        for i in range(self.number):
            average_voltage = np.mean(self.data[self.data.columns[i+1]])
            voltage = (self.voltage_uncertainty[i]/average_voltage)**2

            self.data[self.data.columns[i+1]] = (self.data[self.data.columns[i+1]]/(self.sensitivities[i]/1000))*1000

            sensitivity = (np.mean(self.uncertainty_sensitivity[i]/self.sensitivities))**2
            self.field_uncertainty[i] = np.sqrt((sensitivity+voltage))

        # okay so everything has been calculated, self.data now contains field strengths
        # going to apply the uncertainties to it so that when i split it directionally,
        # I wont also have to split them?

        self.rename_cols()

    def rename_cols(self) -> None:
        '''ds'''

        new_cols = ['time/s']
        new_cols.extend([f'field_strength_S{i}/mT' for i in range(1, self.number +1)])
        self.data.columns = new_cols

        self.data[self.data.columns[0]] = self.data[self.data.columns[0]].astype(float)
        self.data['time/s'] = self.data['time/s']/1000

        #okay now going to attempt to split the field uncertainty and the dataframe

        self.split()

    def split(self) -> None:
        '''ds'''
        # think i will need more if statments for this
        # or here I can use the config file like
        #
        # with open(output_json, encoding = 'utf-8') as f:
        #    sensor_data = json.load(f)
        #
        # for sensor in sensor_data['sensors']:
        #   if sensor['direction'] == 'x':
        #       number = sensor['number'] # would be slightly different? (i-1)*3?
        #       self.data[self.data.columns[number]] = x_frame[x_frame.column[i+1??]]
        # not sure about the indexing yet but i think this concept could work?
        # other option is to split everything into three datasets (self.data_x. self.data_y, self.data_z)
        # and just deal with them separatelt the whole time (basically just do 3x 1D calibrations)
        # That might be easier I am not actually sure.

        # am thinking im just going to do this one manually, and then for the next attempt i can try
        # to use the config file all the way through.

        # lets make new data frames to put them in

        rows = self.data.shape[0]

        self.data_x = pd.DataFrame(np.zeros((rows, int(self.number/3))), dtype = float)
        self.data_y = pd.DataFrame(np.zeros((rows, int(self.number/3))), dtype = float)
        self.data_z = pd.DataFrame(np.zeros((rows, int(self.number/3))), dtype = float)

        self.field_uncertainty_x = np.empty(int(self.number/3))
        self.field_uncertainty_y = np.empty(int(self.number/3))
        self.field_uncertainty_z = np.empty(int(self.number/3))


        # currently the uncertainties are stored in an array, length self.number
        # one for each (surely they will need to be in a dataframe as well????)
        # no its fine actually, the uncertainties will be stored as a percentage
        # of the field, each sensor/column will have its own percentage

        for i in range(self.number):
            if i%3 == 0: # z data, x uncertainties
                # split dataframe
                self.data_z[self.data_z.columns[0]] = self.data[self.data.columns[0]]
                self.data_z[self.data_z.columns[i/3]] = self.data[self.data.columns[i+1]]

                #split uncertainties
                self.field_uncertainty_x[i/3] = self.field_uncertainty[i]


            if i%3 == 1: # y data, z uncertainties
                #split dataframe
                self.data_y[self.data_y.columns[0]] = self.data[self.data.columns[0]]
                self.data_y[self.data_y.columns[(i+1)/3]] = self.data[self.data.columns[i+1]]

                #split uncertainties
                self.field_uncertainty_z[(i-2)/3] = self.field_uncertainty[i]

            if i%3 == 2: # x data, y uncertainties
                #split dataframe
                self.data_x[self.data_x.columns[0]] = self.data[self.data.columns[0]]
                self.data_x[self.data_x.columns[(i+2)/3]] = self.data[self.data.columns[i+1]]

                #split uncertainties
                self.field_uncertainty_y[(i-1)/3] = self.field_uncertainty[i]
        self.display()


    def display(self) -> None:
        '''ds'''
        # now that i have them split, i just want to display them separately - then i will test the code!

        field_display_x = self.data_x.copy()
        field_display_y = self.data_y.copy()
        field_display_z = self.data_z.copy()

        for i in range(self.number):
            column_x = field_display_x.columns[i+1]
            column_y = field_display_y.columns[i+1]
            column_z = field_display_z.columns[i+1]

            uncertainty_x = self.field_uncertainty_x[i]
            uncertainty_y = self.field_uncertainty_y[i]
            uncertainty_z = self.field_uncertainty_z[i]

            field_display_x[column_x] = field_display_x[column_x].apply(lambda x: f'{x:.3f} ± {abs(x*uncertainty_x):.3f}')
            field_display_y[column_y] = field_display_y[column_y].apply(lambda x: f'{x:.3f} ± {abs(x*uncertainty_y):.3f}')
            field_display_z[column_z] = field_display_z[column_z].apply(lambda x: f'{x:.3f} ± {abs(x*uncertainty_z):.3f}')

        print("x-fields")
        print(field_display_x)
        print("y-fields")
        print(field_display_y)
        print("z-fields")
        print(field_display_z)
