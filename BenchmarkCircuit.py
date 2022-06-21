from locale import ABDAY_1, ABMON_10
from Box2D import *
from CarPhysics.Car import MovingCar,FreeCar,WaypointsCar
from CarPhysics.WayPoints import Trajectory


class BenchmarkCircuit_Crossing :

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


class BenchmarkCircuit_8 :

    def __init__(self,world):
        self.world = world

        # flat world: no gravity here
        world.gravity=(0,0)

        # utility vectors
        N = b2Vec2(0,1)
        S = b2Vec2(0,-1)
        E = b2Vec2(1,0)
        W = b2Vec2(-1,0)
        NE = N + E
        NW = N + W
        SE = S + E
        SW = S + W

        # 8-shape
        #       d---e
        #       |   |
        #   a---o---f
        #   |   |
        #   b---c
        l = 30 # half road length
        w = 9  # half-road width
        _a = b2Vec2(-l,0)
        _b = b2Vec2(-l,-l)
        _c = b2Vec2(0,-l)
        _d = b2Vec2(0,l)
        _e = b2Vec2(l,l)
        _f = b2Vec2(l,0)

        # street borders and trajectory points
        # a0-------------------border 
        # |  a1----------------lane 1 
        # |  |  a2-------------lane 2  
        # |  |  |  a-----------center
        # |  |  |  |  a3-------lane 3 
        # |  |  |  |  |  a4----lane 4 
        # |  |  |  |  |  |  a5-border 
        # |  |  |  |  |  |  | 
        a = [_a+NW*w , _a+NW*w*0.75 ,  _a+NW*w*0.25 , _a+SE*w*0.25 , _a+SE*w*0.75 , _a+SE*w ]
        b = [_b+SW*w , _b+SW*w*0.75 ,  _b+SW*w*0.25 , _b+NE*w*0.25 , _b+NE*w*0.75 , _b+NE*w ]
        c = [_c+SE*w , _c+SE*w*0.75 ,  _c+SE*w*0.25 , _c+NW*w*0.25 , _c+NW*w*0.75 , _c+NW*w ]
        d = [_d+SE*w , _d+SE*w*0.75 ,  _d+SE*w*0.25 , _d+NW*w*0.25 , _d+NW*w*0.75 , _d+NW*w ]
        e = [_e+SW*w , _e+SW*w*0.75 ,  _e+SW*w*0.25 , _e+NE*w*0.25 , _e+NE*w*0.75 , _e+NE*w ]
        f = [_f+NW*w , _f+NW*w*0.75 ,  _f+NW*w*0.25 , _f+SE*w*0.25 , _f+SE*w*0.75 , _f+SE*w ]

        trajectories=[]
        trajectories.append(Trajectory([a[1],b[1],c[1],d[1],e[1],f[1],a[1]]))
        trajectories.append(Trajectory([a[2],b[2],c[2],d[2],e[2],f[2],a[2]]))
        trajectories.append(Trajectory([a[3],f[3],e[3],d[3],c[3],b[3],a[3]]))
        trajectories.append(Trajectory([a[4],f[4],e[4],d[4],c[4],b[4],a[4]]))

        

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
        # for initialtrip in [0.0,l-3]:
        #     self.cars.append(MovingCar(world=self.world,initialpos=(-w*0.75,l-3),endpos=(-w*0.75,-l+3),speed=15,initialtrip=initialtrip))
        #     self.cars.append(MovingCar(world=self.world,initialpos=(-w*0.25,l-3),endpos=(-w*0.25,-l+3),speed=25,initialtrip=initialtrip))
        #     self.cars.append(MovingCar(world=self.world,initialpos=(w*0.75,-l+3),endpos=(w*0.75,l-3),speed=15,initialtrip=initialtrip))
        #     self.cars.append(MovingCar(world=self.world,initialpos=(w*0.25,-l+3),endpos=(w*0.25,l-3),speed=25,initialtrip=initialtrip))
 
        #     self.cars.append(MovingCar(world=self.world,initialpos=(l-3,-w*0.75),endpos=(-l+3,-w*0.75),speed=15,initialtrip=initialtrip+(l-3)/2))
        #     self.cars.append(MovingCar(world=self.world,initialpos=(l-3,-w*0.25),endpos=(-l+3,-w*0.25),speed=25,initialtrip=initialtrip+(l-3)/2))
        #     self.cars.append(MovingCar(world=self.world,initialpos=(-l+3,w*0.75),endpos=(l-3,w*0.75),speed=15,initialtrip=initialtrip+(l-3)/2))
        #     self.cars.append(MovingCar(world=self.world,initialpos=(-l+3,w*0.25),endpos=(l-3,w*0.25),speed=25,initialtrip=initialtrip+(l-3)/2))

        # self.cars.append(WaypointsCar(world=self.world,trajectory=Trajectory([(-w*0.75,l-3),(-w*0.75,-l+3),(w*0.75,-l+3),(w*0.75,l-3),(-w*0.75,l-3)]),speed=25))
        nbCarsperTrack = 5

        for lane in range(4):
            for c in range(nbCarsperTrack):
                initialTrip = c*trajectories[lane].length/nbCarsperTrack
                self.cars.append( WaypointsCar(world=self.world,trajectory=trajectories[lane],speed=25,initialtrip=initialTrip) )

        self.freeCar = FreeCar(self.world,w/4,w*2)
        self.cars.append(self.freeCar)

    def Step(self,timeStep):
        # timeStep in seconds
        for car in self.cars:
            car.Step(timeStep)
        return        