# from Box2D.examples.framework import (Framework, main)

from concurrent.futures.thread import _global_shutdown_lock
from tkinter import E
from Box2D import *
from Box2D.examples.framework import (Framework, Keys, main)

from time import time

from CarPhysics import MovingCar,FreeCar


class Benchmark :

    def __init__(self,world):
        self.world = world

        # flat world: no gravity here
        world.gravity=(0,0)

        # fixed obstacles :

        # cross intersection shape
        w = 9  # half-road width
        l = 30 # half road length
        #   A B
        # K L C D
        # J I F E
        #   H G
        A = (-w,l)
        B = (w,l)
        C = (w,w)
        D = (l,w)
        E = (l,-w)
        F = (w,-w)
        G = (w,-l)
        H = (-w,-l)
        I = (-w,-w)
        J = (-l,-w)
        K = (-l,w)
        L = (-w,w)
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[A,B]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[B,C]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[C,D]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[D,E]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[E,F]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[F,G]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[G,H]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[H,I]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[I,J]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[J,K]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[K,L]))
        self.world.CreateBody(shapes=b2EdgeShape(vertices=[L,A]))

        # carShape = b2PolygonShape(box=(1,2))
        # boxFD = b2FixtureDef(
        #     shape=carShape,
        #     friction=0.2,
        #     density=20,
        # )

        # for x in range(1):
        #     for y in range(1):
        #         body = self.world.CreateDynamicBody(
        #         # body = self.world.CreateBody(
        #             position=(x*4, y*6),
        #             fixtures=boxFD,
        #         )

        self.cars = []
        for initialtrip in [0.0,l-3]:
            self.cars.append(MovingCar(world=self.world,initialpos=(-w*0.75,l-3),endpos=(-w*0.75,-l+3),speed=15,initialtrip=initialtrip))
            self.cars.append(MovingCar(world=self.world,initialpos=(-w*0.25,l-3),endpos=(-w*0.25,-l+3),speed=25,initialtrip=initialtrip))
            self.cars.append(MovingCar(world=self.world,initialpos=(w*0.75,-l+3),endpos=(w*0.75,l-3),speed=15,initialtrip=initialtrip))
            self.cars.append(MovingCar(world=self.world,initialpos=(w*0.25,-l+3),endpos=(w*0.25,l-3),speed=25,initialtrip=initialtrip))
 
            self.cars.append(MovingCar(world=self.world,initialpos=(l-3,-w*0.75),endpos=(-l+3,-w*0.75),speed=15,initialtrip=initialtrip+(l-3)/2))
            self.cars.append(MovingCar(world=self.world,initialpos=(l-3,-w*0.25),endpos=(-l+3,-w*0.25),speed=25,initialtrip=initialtrip+(l-3)/2))
            self.cars.append(MovingCar(world=self.world,initialpos=(-l+3,w*0.75),endpos=(l-3,w*0.75),speed=15,initialtrip=initialtrip+(l-3)/2))
            self.cars.append(MovingCar(world=self.world,initialpos=(-l+3,w*0.25),endpos=(l-3,w*0.25),speed=25,initialtrip=initialtrip+(l-3)/2))

        self.freeCar = FreeCar(self.world,w/4,w*2)
        self.cars.append(self.freeCar)

    def Step(self,timeStep):
        # timeStep in seconds
        for car in self.cars:
            car.Step(timeStep)
        return


class BenchFramework (Framework):
    name = "Collision benchmark framework"
    # description = "Press j to toggle the rope joint."

    def __init__(self):
        super(BenchFramework, self).__init__()

        # visual settings...
        # self.settings.pause = True
        # self.settings.drawMenu = False

        # create a benchmark... 
        self.benchmark = Benchmark(self.world)
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
        bench = Benchmark(world)
        nbSteps = 100000
        t0 = time()
        for i in range(nbSteps):
            bench.Step(1.0/60)
        dt = time() - t0
        freq = float(nbSteps) / dt
        print(f"Steps={nbSteps} Freq={freq}")
