from manim import *
import math

class interactiveDemo(ThreeDScene):
    

    def construct(self):
       # Set up the axes
        axes = ThreeDAxes()

        # Create a vector field
        vector_field = ArrowVectorField(
            lambda p: np.array([-p[1], p[0], np.sin(p[0] + p[1]) - p[2]]), 
            x_range=[-3, 3,1], 
            y_range=[-3, 3,1],
            z_range=[-3, 3,0.5]
        )

        # Add axes and vector field to the scene
        self.add(axes, vector_field)

        # Set the camera angle
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(90*DEGREES/6, about='theta')
        # Show the scene
        self.play(Create(vector_field))
        self.wait(20)