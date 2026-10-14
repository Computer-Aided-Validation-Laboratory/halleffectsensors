from pathlib import Path
import pandas as pd
import numpy as np

data = pd.DataFrame(np.zeros((10,10)), dtype = float)
current_file = Path(__file__).parent / 'csv' / 'csv1'
data.to_csv(current_file, index = False)

current_file = Path(__file__).parent / 'csv' / 'csv1'

#current_file.parent.mkdir(parents = True, exist_ok = True)
