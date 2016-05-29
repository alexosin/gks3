import circle
import sys

circle1 = circle.CirclePath((70, 85), 30)
#circle1.plot_circle()
circle1.get_path_by_interpolation_predict(1, True)
