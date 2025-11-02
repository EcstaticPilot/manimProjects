from manim import *
import math
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
    
    def intro(self):
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
        
    def construct(self):
        
        self.intro()

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
        self.clear()
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
        tangentText = Text("Tangent Lines").shift(UP*3)
        self.play(Write(tangentText))
        d1.set_z_index(l1b.z_index+1)
        d2.set_z_index(l1b.z_index+1)
        d3.set_z_index(l3b.z_index+1)
        d3.set_z_index(l3b.z_index+1)
        self.play(Transform(l1,l1b),Transform(l3,l3b), run_time = 0.5)
        self.play(Transform(l1b,l1),Transform(l3b,l3), run_time = 0.5)
        self.play(FadeOut(tangentText))
        self.pause()
        self.remove(l1b,l3b)
        d1.target.shift(DOWN*3 + LEFT)
        d2.target.shift(UP*2+LEFT*3)
        d3.target.shift(DOWN)
        d4.target.shift(RIGHT*3+DOWN)
        bezier.target.become(CubicBezier(d1.target.get_center(),d2.target.get_center(),d3.target.get_center(),d4.target.get_center()))
        self.play(MoveToTarget(d1),MoveToTarget(d2),MoveToTarget(d3),MoveToTarget(d4),MoveToTarget(bezier))
        self.pause()
        # l2b = Line(d2.get_center(),d3.get_center()).set_color(GRAY)
        # self.add(l2b)
        # self.remove(l1,l2,l3)
        l1.clear_updaters()
        l2.clear_updaters()
        l3.clear_updaters()
        self.play(Uncreate(l1),Uncreate(l2),Uncreate(l3),Uncreate(d1),Uncreate(d2),Uncreate(d3),Uncreate(d4))
        
        self.pause()
        #robot.scale(0.5)
        robot.move_to(bezier.point_from_proportion(0.30))
        tangentAngle  = TangentLine(bezier, alpha=0.30).get_unit_vector()
        robot.shift(2*tangentAngle[1]*LEFT + 2*tangentAngle[0]*UP)
        print(tangentAngle[0])
        print(tangentAngle[1])
        print(tangentAngle[2])
        robot.rotate(-PI/4)
        self.play(Write(robotBody), Write(wheel1), Write(wheel2), Write(wheel3), Write(wheel4))
        
        self.pause()
        tangent = TangentLine(bezier, alpha=0.30,length = 4).set_color(RED)
        tangentText = Text('Tangent Line').shift(RIGHT*4.5+UP*3).set_color(RED)
        crosstrack = Line(robot.get_center(),bezier.point_from_proportion(0.30)).flip(LEFT).flip(UP).set_color(BLUE)
        crosstrackText = Text('Cross Track Error').set_color(BLUE).shift(RIGHT*4+UP*2)
        #LDdimension  = DoubleArrow(tip_shape_end = BarTip)
        self.play(Create(tangent),Write(tangentText))
        self.pause()
        self.play(Create(crosstrack),Write(crosstrackText))
        self.play(tangent.animate.shift(tangentAngle*2))
        robotHeadingLine = Line(robot.get_center(),robot.get_center()+UP*2+RIGHT*2)
        self.play(Create(robotHeadingLine))
        
        LDline = Line(crosstrack.get_end(),tangent.get_end()).set_color(YELLOW)
        self.play(Create(LDline))
        arc1 = Arc(1,PI/4,angle_of_vector(tangentAngle)-PI/4,arc_center=robot.get_center()).set_color(GREEN)
        
        self.play(tangent.animate.move_to(robot.get_center()+2*tangentAngle))
        self.play(Create(arc1))
        self.play(crosstrack.animate.shift(tangentAngle * 4))
        
        arc2 = Arc(1,angle_of_vector(tangentAngle),angle_of_vector(LDline.get_unit_vector())-angle_of_vector(tangentAngle), arc_center=robot.get_center()).set_color(PURPLE)
        self.play(Create(arc2))
        self.pause()
        all_mobjects = Group(*self.mobjects)  # Create a group of all mobjects
    #     for mobject in all_mobjects:
    #         if(mobject.name == 'Text'):
    #             #all_mobjects.remove(mobject)
    #    # all_Text = Group(tangentText,crosstrackText)
        self.play(all_mobjects.animate.shift(ORIGIN-robot.get_center_of_mass()), run_time=2)
        self.pause()
        self.play(Rotate(all_mobjects, angle=PI/4, about_point=ORIGIN),run_time=2)
        self.pause()
        self.play(FadeOut(bezier))
        arc2.generate_target()
        arc2.target.start_angle = -PI/4
        arc3 = Arc(1,PI/2,-PI/2+angle_of_vector(LDline.get_unit_vector()),arc_center=robot.get_center()).set_color(BLUE)
        
        LDline.generate_target()
        LDline.target =Line(robot.get_center(),  robot.get_center() + 2*LDline.get_unit_vector()).set_color(YELLOW)
        
        self.play(Create(arc3), MoveToTarget(LDline), FadeOut(arc1,arc2,crosstrack,tangent))
        self.pause()
        self.play(Group(LDline,robotHeadingLine,arc3).animate.shift(UP*1))
        center = (arc3.get_arc_center()[1]/math.cos(angle_of_vector(LDline.get_unit_vector())+PI/2) * LEFT)
        centerpt = Dot(center)
        line1 = Line(arc3.get_arc_center(),center)
        #delta y/cos
        self.pause()
        self.play(Create(line1),Create(centerpt))
        leftCircle = Circle(2.25).shift(center).set_color(ORANGE)
        RightCircle = Circle(0.5).shift(center).set_color(PURPLE)
        leftText = Text("Left Circle").set_color(ORANGE).shift(5*RIGHT+3*UP)
        rightText = Text("Right Circle").set_color(PURPLE).shift(5*RIGHT+2*UP)
        self.play(Create(leftCircle),Create(RightCircle), Write(leftText), Write(rightText))
        self.pause()
        eqtest = Tex(r"$\frac{v_{l} } {v_{r} }\sim \frac{r_{l}}{ {r_{r} } } =$",r"$\frac{2\pi(r+\frac{w}{2})}{2\pi(r-\frac{w}{2})}$").shift(LEFT*5 + UP)
        eq2 = Tex(r"$\frac{v_{l} } {v_{r} }\sim \frac{r_{l}}{ {r_{r} } } =$",r"$\frac{2 \pi r (1+\frac{w}{2r})}{2 \pi r (1-\frac{w}{2r})}$").align_to(eqtest,LEFT).align_to(eqtest,UP)
        eq3 = Tex(r"$\frac{v_{l} } {v_{r} }\sim \frac{r_{l}}{ {r_{r} } } =$",r"$\frac{ (1+\frac{w}{2r})}{ (1-\frac{w}{2r})}$").align_to(eqtest,LEFT).align_to(eqtest,UP)
        eq4 = Tex(r"$v_{l}=$",r"$ v(1+\frac{w}{2r})$").align_to(eqtest,LEFT).align_to(eqtest,UP).shift(DOWN)
        eq5 = Tex(r"$v_{r}=$",r"$ v(1-\frac{w}{2r})$").align_to(eqtest,LEFT).align_to(eqtest,UP).shift(2*DOWN)
        self.play(Write(eqtest))
        self.pause()
        self.play(Transform(eqtest[1],eq2[1]))
        self.pause()
        self.play(Transform(eqtest[1],eq3[1]))
        self.pause()
        self.play(TransformFromCopy(eqtest,eq4))
        self.play(TransformFromCopy(eqtest,eq5))
        # change bezier curve
        
        
       