'''going to attempt to plot each field results? no clue what this will look like but we will see'''

# first need to get our three dataframes containing the field measurements

from pathlib import Path
import pandas as pd

data_path = Path(__file__).parent / 'csv'

x_data = pd.read_csv(data_path / 'x_data.csv')
y_data = pd.read_csv(data_path / 'y_data.csv')
z_data = pd.read_csv(data_path / 'z_data.csv')


# lets just plot the x data first
