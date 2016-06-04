import circle

circle1 = circle.CirclePath((70, 85), 30, T=3, V= 5, step=5)
#circle1.plot_circle()
circle1.get_path_by_interpolation_predict(True)
circle1.method_cont_carrier_freq(True)
circle1.corrections_forecast(True)
