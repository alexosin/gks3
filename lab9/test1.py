import circle

circle1 = circle.CirclePath((0, 0), 55, T=12, V=2.4, step=5)
#circle1.get_path_by_interpolation_predict()
#circle1.method_cont_carrier_freq()
circle1.corrections_forecast(True)
