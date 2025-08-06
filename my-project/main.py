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
        self.play(FadeOut(title,name))
        self.pause(1)
        
        robotBody = Rectangle(height = 3, width=1.5).set_fill(GRAY,opacity=0.25)
        wheel1 = Rectangle(height=1,width=0.5).align_to(robotBody,LEFT) .align_to(robotBody,UP)  .shift(LEFT * 0.5) .set_fill(GRAY,opacity=0.25)
        wheel2 = Rectangle(height=1,width=0.5).align_to(robotBody,LEFT) .align_to(robotBody,DOWN).shift(LEFT * 0.5) .set_fill(GRAY,opacity=0.25)
        wheel3 = Rectangle(height=1,width=0.5).align_to(robotBody,RIGHT).align_to(robotBody,UP)  .shift(RIGHT * 0.5).set_fill(GRAY,opacity=0.25)
        wheel4 = Rectangle(height=1,width=0.5).align_to(robotBody,RIGHT).align_to(robotBody,DOWN).shift(RIGHT * 0.5).set_fill(GRAY,opacity=0.25)
        robot = Group(robotBody,wheel1,wheel2,wheel3,wheel4)
        self.play(Write(robotBody), Write(wheel1), Write(wheel2), Write(wheel3), Write(wheel4), run_time = 2)
        #self.play(Transform(title[8].flip(LEFT),robotBody))
        self.pause(2)
        arrowleftdbl = DoubleArrow(start=robotBody.get_bottom()+DOWN*0.5,end=robotBody.get_top()+UP*0.5).shift(LEFT*2)
        arrowrightdbl= DoubleArrow(start=robotBody.get_bottom()+DOWN*0.5,end=robotBody.get_top()+UP*0.5).shift(RIGHT*2)
        arrowleft = Arrow(start=robotBody.get_bottom()+DOWN*0.5,end=robotBody.get_top()+UP*0.5).shift(LEFT*2)
        arrowright= Arrow(start=robotBody.get_bottom()+DOWN*0.5,end=robotBody.get_top()+UP*0.5).shift(RIGHT*2) 
        self.play(Create(arrowleftdbl), Create(arrowrightdbl))
        self.pause(2)
        self.play(FadeOut(arrowleftdbl,arrowrightdbl), FadeIn(arrowleft,arrowright))
        self.pause(0.1)
        self.play(robot.animate.shift(UP),arrowright.animate.shift(UP),arrowleft.animate.shift(UP))
        self.play(arrowright.animate.flip(LEFT))
        self.play(Rotate(robot,-PI/2), Rotate(arrowleft,-PI/2,about_point=robot.get_center()), Rotate(arrowright,-PI/2,about_point=robot.get_center()),run_time = 2)
        self.play(FadeOut(arrowleft,arrowright))
        self.pause(2)
        
        questionText = Text("???").shift(UP*3)
        p1 = robot.get_center()
        p2 = p1 + [8, 0, 0]
        p4 = np.array([0, -8, 0])  
        p3 = p4 + [0,4, 0]
        bezier = CubicBezier(p1, p2, p3, p4)
        self.play(Write(questionText))
        
        # Tracker for time along the curve
        t = ValueTracker(0)
        prev_angle = [0]
        # Define updater: move + rotate using TangentLine
        def update_robot(mob):
            alpha = t.get_value()

            # Get position on curve
            pos = bezier.point_from_proportion(alpha)

            # Use TangentLine to get direction vector
            tangent_line = TangentLine(bezier, alpha=alpha)
            direction = tangent_line.get_unit_vector()

            # Calculate angle from vector
            angle = angle_of_vector(direction)
            delta = angle - prev_angle[0]
            prev_angle[0] = angle
            # Move and rotate robot (adjust if robot "faces" up)
            mob.move_to(pos)
            mob.rotate(delta)  # Adjust because robot faces UP

        # Add the updater
        robot.add_updater(update_robot)
        
        # Animate from t = 0 to 1
        self.play(t.animate.set_value(1), run_time=3)

        # Optional: stop updating
        robot.clear_updaters()
        self.play(FadeOut(questionText))
        self.wait(3)

        #* bezier curve
        p1 = np.array([-3, 1, 0]) 
        p2 = p1 + [2, 0, 0] 
        d1 = Dot(point=p1).set_color(BLUE) 
        l1 = Line(p1, p2).set_color(GRAY) 
        p4 = np.array([3, -1, 0]) 
        p3 = p4 - [2, 0, 0] 
        d4 = Dot(point=p4).set_color(RED) 
        l2 = Line(p3, p4).set_color(GRAY) 
        l3 = Line(p2,p3).set_color(GRAY)
        d2 = Dot(point=p2).set_color(GREEN)
        d3 = Dot(point=p3).set_color(YELLOW)
        bezier = CubicBezier(p1, p2, p3, p4)

        bezierText = Text('Bezier Curve', font_size = 100).shift(UP*3)
        
        self.play(Create(bezier),Create(l1),Create(l2), Create(l3), Create(d1), Create(d2),Create(d3),Create(d4), Write(bezierText),run_time = 3)
        l1.add_updater(lambda x: x.become(Line(d1.get_center(), d2.get_center()).set_color(GRAY)))
        l2.add_updater(lambda x: x.become(Line(d2.get_center(), d3.get_center()).set_color(GRAY)))
        l3.add_updater(lambda x: x.become(Line(d3.get_center(), d4.get_center()).set_color(GRAY)))
        self.pause(2)
        factor = 2
        self.play(ScaleInPlace(d1,factor),ScaleInPlace(d2,factor),ScaleInPlace(d3,factor),ScaleInPlace(d4,factor),run_time = 0.5)
        self.play(ScaleInPlace(d1,1/factor),ScaleInPlace(d2,1/factor),ScaleInPlace(d3,1/factor),ScaleInPlace(d4,1/factor),run_time = 0.5)
        self.pause(1)
        
        # animate moving them around (setup)
        d2.generate_target()
        d3.generate_target()
        bezier.generate_target()
        
        #move targets, there is potentially a better way using an updater on the bezier object
        d2.target.shift(UP+RIGHT)
        d3.target.shift(DOWN+LEFT)
        
        bezier.target.become(CubicBezier(p1,d2.target.get_center(),d3.target.get_center(),p4))
        self.play(MoveToTarget(d2),MoveToTarget(d3),MoveToTarget(bezier))
        self.pause()
        
        # part 2
        d2.target.shift(DOWN*4 + LEFT)
        d3.target.shift(UP*4 + RIGHT)
        
        bezier.target.become(CubicBezier(p1,d2.target.get_center(),d3.target.get_center(),p4))
        self.play(MoveToTarget(d2),MoveToTarget(d3),MoveToTarget(bezier))
        self.pause()
        
        d1.generate_target()
        d4.generate_target()
        d1.target.shift(LEFT + DOWN)
        d4.target.shift( UP+RIGHT)
        
        bezier.target.become(CubicBezier(d1.target.get_center(),d2.get_center(),d3.get_center(),d4.target.get_center()))
        self.play(MoveToTarget(d1),MoveToTarget(d4),MoveToTarget(bezier))
        self.pause()
        
        
        self.play(FadeOut(bezierText))
        
        #explain end pointsa nd control
        factor = 3
        endpointsText = Text("Anchor/End Points").shift(UP*3)
        self.play(Write(endpointsText))
        self.play(ScaleInPlace(d1,factor),ScaleInPlace(d4,factor),run_time = 0.5)
        self.play(ScaleInPlace(d1,1/factor),ScaleInPlace(d4,1/factor),run_time = 0.5)
        self.play(FadeOut(endpointsText))
        controlpointsText = Text("Handle Points").shift(UP*3)
        self.play(Write(controlpointsText))
        self.play(ScaleInPlace(d2,factor),ScaleInPlace(d3,factor),run_time = 0.5)
        self.play(ScaleInPlace(d2,1/factor),ScaleInPlace(d3,1/factor),run_time = 0.5)
        self.play(FadeOut(controlpointsText))
        
        
        l1b = Line(d1.get_center(),d2.get_center(), stroke_width = 20).set_color(GRAY)
        l3b = Line(d3.get_center(),d4.get_center(), stroke_width = 20).set_color(GRAY)
        self.play(Transform(l1,l1b),Transform(l3,l3b))
        self.play(Transform(l1b,l1),Transform(l3b,l3))
        self.pause()

        # change bezier curve
        
        
       