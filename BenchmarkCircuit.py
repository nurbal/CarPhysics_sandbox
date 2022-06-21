from Box2D import *
from CarPhysics.Car import MovingCar,FreeCar,WaypointsCar
from CarPhysics.WayPoints import Trajectory


class BenchmarkCircuit :

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
            # self.cars.append(MovingCar(world=self.world,initialpos=(-w*0.75,l-3),endpos=(-w*0.75,-l+3),speed=15,initialtrip=initialtrip))
            # self.cars.append(MovingCar(world=self.world,initialpos=(-w*0.25,l-3),endpos=(-w*0.25,-l+3),speed=25,initialtrip=initialtrip))
            # self.cars.append(MovingCar(world=self.world,initialpos=(w*0.75,-l+3),endpos=(w*0.75,l-3),speed=15,initialtrip=initialtrip))
            # self.cars.append(MovingCar(world=self.world,initialpos=(w*0.25,-l+3),endpos=(w*0.25,l-3),speed=25,initialtrip=initialtrip))
 
            # self.cars.append(MovingCar(world=self.world,initialpos=(l-3,-w*0.75),endpos=(-l+3,-w*0.75),speed=15,initialtrip=initialtrip+(l-3)/2))
            # self.cars.append(MovingCar(world=self.world,initialpos=(l-3,-w*0.25),endpos=(-l+3,-w*0.25),speed=25,initialtrip=initialtrip+(l-3)/2))
            # self.cars.append(MovingCar(world=self.world,initialpos=(-l+3,w*0.75),endpos=(l-3,w*0.75),speed=15,initialtrip=initialtrip+(l-3)/2))
            # self.cars.append(MovingCar(world=self.world,initialpos=(-l+3,w*0.25),endpos=(l-3,w*0.25),speed=25,initialtrip=initialtrip+(l-3)/2))

            self.cars.append(WaypointsCar(world=self.world,trajectory=Trajectory([(-w*0.75,l-3),(-w*0.75,-l+3),(w*0.75,-l+3),(w*0.75,l-3),(-w*0.75,l-3)]),speed=25))

        self.freeCar = FreeCar(self.world,w/4,w*2)
        self.cars.append(self.freeCar)

    def Step(self,timeStep):
        # timeStep in seconds
        for car in self.cars:
            car.Step(timeStep)
        return