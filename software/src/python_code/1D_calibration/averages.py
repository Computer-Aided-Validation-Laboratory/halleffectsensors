# so gonna take an average of each sensor over all the 8 fields
# and see if the average goes up
# i think the calculation is wrong though because 4 and 4 again
# they have completely different sensitivities even in the same
# field, sensitivity should be independent of the field
# something has gone wrong!
# but now that i have a bunch of data maybe I should attempt to
# do the calculations by hand and just see if i get the same
# answer or not!

# lets start with 8A - pretty happy with the nulls, think that works
# the fact that my sensitivities are in the thousands is not a good
# sign i don't think!

import pandas as pd
import numpy as np
from pathlib import Path

csvpath = Path(__file__).resolve().with_name('calibration_1_A.csv')
dataframe = pd.read_csv(csvpath)

for i in range(7):
    average_sensor_reading = np.mean(dataframe[dataframe.columns[i+1]])