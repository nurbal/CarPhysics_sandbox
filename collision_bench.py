# from Box2D.examples.framework import (Framework, main)

from concurrent.futures.thread import _global_shutdown_lock
from tkinter import E
from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import *
from time import time
from tqdm import tqdm

from BenchmarkCircuit import BenchmarkCircuit_Crossing, BenchmarkCircuit_8


class BenchFramework (Framework):
    name = "Collision benchmark framework"
    # description = "Press j to toggle the rope joint."

    def __init__(self):
        super(BenchFramework, self).__init__()

        # visual settings...
        # self.settings.pause = True
        # self.settings.drawMenu = False

        # create a benchmark... 
        self.benchmark = BenchmarkCircuit_8(self.world)
        # self.benchmark = BenchmarkCircuit_Crossing(self.world)
        self.freecar = self.benchmark.freeCar

    def Step(self, settings):
        super(BenchFramework, self).Step(settings)

        # Don't do anything if the setting's Hz are <= 0
        if not settings.pause:
            if settings.hz > 0.0:
                timeStep = 1.0 / settings.hz
                self.benchmark.Step(timeStep)

    def Keyboard(self, key):
        if key == Keys.K_w:
            # throttle
            self.freecar.Throttle(1)
        if key == Keys.K_s:
            # reverse
            self.freecar.Throttle(-1)
        if key == Keys.K_LSHIFT:
            # break
            self.freecar.Break(1)
        turn=0
        if key == Keys.K_a:
            # turn left
            turn -= 1
        if key == Keys.K_d:
            # turn right
            turn += 1
        self.freecar.Turn(turn)




if __name__ == "__main__":
    pygame_gui = True
    if pygame_gui:
        # play the scene on pybox2d pygame test framework
        main(BenchFramework)
    else:
        # just run headless and time it !
        world = b2World()
        bench = BenchmarkCircuit_Crossing(world)

        nbSteps = 0
        t0 = time()
        for _ in tqdm(range(10)):
            t = time()
            while (time() - t <1):
                bench.Step(1.0/60)
                nbSteps+=1
        dt = time() - t0
        freq = float(nbSteps) / dt
        print(f"Steps={nbSteps} Freq={freq}")
