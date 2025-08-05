from manim import *
"""
script idea

robot exists
define the problem
robot needs to mvoe on curved path
mention splines
pick bezier
now that we have bezier, how do we follow it
introduce stnaley
how does stanley work
how do we find the things necesary for stanley
convert ackermann to differential
"""


class DefaultTemplate(Scene):
    def construct(self):
        #self.add(NumberPlane().add_coordinates())

        #test2 = CubicBezier([0,0,0],[1,0,0],[0,1,0],[1,1,1],)
        #test2.add()
        title = Text('Stanley Controller',font_size = 100)
        title.shift(UP*3)
        self.play(Write(title,run_time = 3))
        name = Text("Made by Nikhil Ramanuja").shift(DOWN*3)
        self.play(Write(name))
        self.pause(2)
        self.play(FadeOut(title), FadeOut(name))
        self.pause(1)
        
        robotBody = Rectangle(height = 3, width=1.5).set_fill(GRAY,opacity=0.25)
        wheel1 = Rectangle(height=1,width=0.5).align_to(robotBody,LEFT) .align_to(robotBody,UP)  .shift(LEFT * 0.5) .set_fill(GRAY,opacity=0.25)
        wheel2 = Rectangle(height=1,width=0.5).align_to(robotBody,LEFT) .align_to(robotBody,DOWN).shift(LEFT * 0.5) .set_fill(GRAY,opacity=0.25)
        wheel3 = Rectangle(height=1,width=0.5).align_to(robotBody,RIGHT).align_to(robotBody,UP)  .shift(RIGHT * 0.5).set_fill(GRAY,opacity=0.25)
        wheel4 = Rectangle(height=1,width=0.5).align_to(robotBody,RIGHT).align_to(robotBody,DOWN).shift(RIGHT * 0.5).set_fill(GRAY,opacity=0.25)
        robot = Group(robotBody,wheel1,wheel2,wheel3,wheel4)
        self.play(Create(robotBody), Create(wheel1), Create(wheel2), Create(wheel3), Create(wheel4), run_time = 2)
        #self.play(Transform(title[8].flip(LEFT),robotBody))
        self.pause(2)
        arrowleft = DoubleArrow(start=robotBody.get_bottom()+DOWN*0.5,end=robotBody.get_top()+UP*0.5).shift(LEFT*2)
        arrowright= DoubleArrow(start=robotBody.get_bottom()+DOWN*0.5,end=robotBody.get_top()+UP*0.5).shift(RIGHT*2)
        self.play(Create(arrowleft), Create(arrowright))
        self.pause(2)
        self.play(FadeOut(arrowleft), FadeOut(arrowright))
        self.play(robot.animate.shift(UP))
        self.play(Rotate(robot,-PI/2))
        
        
        self.pause(2)
        # bezier curve
        # p1 = np.array([-3, 1, 0]) 
        # p2 = p1 + [2, 0, 0] 
        # d1 = Dot(point=p1).set_color(BLUE) 
        # l1 = Line(p1, p2).set_color(BLUE) 
        # p4 = np.array([3, -1, 0]) 
        # p3 = p4 - [2, 0, 0] 
        # d2 = Dot(point=p4).set_color(RED) 
        # l2 = Line(p3, p4).set_color(RED) 
        # l3 = Line(p2,p3).set_color(GREEN)
        # bezier = CubicBezier(p1, p2, p3, p4)
       
        # bezierText = Text('Bezier Curve', font_size = 100).shift(UP*3)
        
        # self.play(Create(bezier),Create(l1),Create(l2), Create(l3), Create(d1), Create(d2), Write(bezierText),run_time = 3)
        # self.pause(5)
        
       