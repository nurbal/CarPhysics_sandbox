# this file is there only to test python stuff


# a=3
# if a>0 and a<2:
#     print("test")


from shutil import ExecError
import Box2D as b2
# from Car import MovingCar,FreeCar
from CarPhysics.Car import MovingCar,FreeCar


# def InitFreeCar():
#     # helper...
#     world = b2.b2World()
#     world.gravity=(0,0)
#     freeCar = FreeCar(world,4,10)
#     return (world,freeCar)

# (world,car) = InitFreeCar()





from CarPhysics.WayPoints import Trajectory

def InitTriangularTrajectory():
    # triangle rectangle de côtés 3,4,5
    A = b2.b2Vec2(0,0)
    B = b2.b2Vec2(4,0)
    C = b2.b2Vec2(0,3)
    return Trajectory([A,B,C,A])

t = InitTriangularTrajectory()
print (t)

(position,angle) = t.GetPositionAngle(10)
print ((position,angle))

