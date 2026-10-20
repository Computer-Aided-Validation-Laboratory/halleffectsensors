'''runs the calibration software, can be run as many times as there are clibartion fields (
more testing is better resuts)'''

from sens import Sensitivity

#field input in mT
x = Sensitivity(number = 6, port = '/dev/ttyUSB0', vcc = 5, vcc_un = 0.05,
                filename = 'cal_10(9-12)(9.9-6).csv', bits = 10, samples = 400, calibration_field = 9.9,
                field_uncertainty = 0.005)

#x.current_comparison(current=, current_uncertainty=, number_of_turns=, coil_radius=)
x.perform_calibration()
