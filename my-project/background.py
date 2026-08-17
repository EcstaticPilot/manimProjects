from manim import *
import math
DIAG1 = LEFT*math.sqrt(3)/2 + UP*0.5
DIAG1P = UP*math.sqrt(3)/2 + RIGHT*0.5
DIAG2 = LEFT*math.sqrt(3)/2 + DOWN*0.5
DIAG2P = DOWN*math.sqrt(3)/2 + RIGHT*0.5
config.frame_size = (1080, 1920)
SCALE = 1
RUN_TIME = 0.1
class DefaultTemplate(Scene):

    
    def SimultaneousWrite(self,vmobjects: list[Triangle]):
        
        buffer:list[Animation] = []
        for e in vmobjects:
            buffer.append(Write(e))
        self.play(*buffer,run_time = RUN_TIME)
        
    def triangleExists(self, list, triangle:Triangle):
        for e in list:
            if np.linalg.norm((e.get_center() - triangle.get_center())) < 0.1:
                return True
        return False
    def generateTriangles(self,t:Triangle,up:bool):
        #newT = t.copy().rotate(PI,about_point=t.get_center_of_mass())
        if up:
            newT = Triangle(color = ORANGE).scale(SCALE).move_to(t.get_center())
            newT.rotate(PI,about_point=newT.get_center_of_mass())
            return [newT.copy().shift(DIAG1*SCALE),newT.copy().rotate(4*PI/3,about_point=t.get_center_of_mass()).shift(-DIAG2*SCALE),newT.copy().rotate(2*PI/3,about_point=t.get_center_of_mass()).shift(DOWN*SCALE)]
              
        newT = Triangle(color = ORANGE).scale(SCALE).rotate(PI).move_to(t.get_center())
        newT.rotate(-PI,about_point=newT.get_center_of_mass())       
        return [newT.copy().rotate(4*PI/3,about_point=t.get_center_of_mass()).shift(UP*SCALE),newT.copy().rotate(2*PI/3,about_point=t.get_center_of_mass()).shift(-DIAG1*SCALE),newT.copy().shift(DIAG2*SCALE)]                 
    
    
    def construct(self):
        #start2 = start.copy().flip(RIGHT).shift(UP*0.76)
        #start2 = start.copy().flip(RIGHT).shift(RIGHT*0.42)
        
       #$ start2 = start.copy().rotate(PI,about_point=start.get_center_of_mass()).shift(DIAG1*0.5)
        #start3 = start2.copy().rotate(PI,about_point=start2.get_center_of_mass()).shift(DIAG1*0.5)

        #start2 = start.copy().flip(UP,about_edge=RIGHT)
        #self.play(Write(start.copy().flip(UP).shift(-DIAG1P*0.75)),Write(start.copy().flip(UP).shift(RIGHT*0.75)),Write(start.copy().flip(UP).shift(-DIAG2P*0.75)))
        
        #self.play(Write(start.copy().flip(DIAG1,about_edge=DIAG2P),reverse=True),Write(start.copy().flip(DIAG2,about_edge=DIAG1P),reverse=True),Write(start.copy().flip(UP,about_edge=DIAG2P)))
        
        existing:list[Triangle] = []
        frontier:list[Triangle] = []
        
        start = Triangle(color=ORANGE).scale(SCALE)
        start2 = start.copy().rotate(PI)
        existing.append(start)
        frontier.append(start)
        self.play(Write(start),run_time = RUN_TIME)
        flag = True
        
        for _ in range(20):
            buffer:list[Triangle] = []
            for t in frontier:
                for nt in self.generateTriangles(t,flag):
                    if self.triangleExists(existing+buffer,nt) == False:
                        buffer.append(nt)
            self.SimultaneousWrite(buffer)
            frontier = buffer
            flag = not flag
        self.pause(5)
                        
