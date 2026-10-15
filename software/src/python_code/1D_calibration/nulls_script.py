'''runs the calculation of the null voltage and standard deviation for each sensor'''

from nulls import Nulls

x = Nulls(number = 6 ,port = '/dev/ttyUSB0', vcc = 5.0,
          filename = 'calibration.csv', vcc_un = 0.05, bits = 10, samples = 400)
