from manim import *

class MoveAlongPathExample(Scene):
    def construct(self):
        p1 = np.array([-3, 1, 0])
        p2 = p1 + [2, 0, 0]
        p4 = np.array([3, -1, 0])  
        p3 = p4 - [2, 0, 0]
        bezier = CubicBezier(p1, p2, p3, p4)
        d1 = Dot().set_color(ORANGE)
        l1 = Line(LEFT, RIGHT)
        l2 = VMobject()
        self.add(d1, l1,l2)
        l2.add_updater(lambda x: x.become(Line(LEFT, d1.get_center()).set_color(ORANGE)))
        self.add(bezier)
        self.play(MoveAlongPath(d1, bezier), rate_func=linear)
        