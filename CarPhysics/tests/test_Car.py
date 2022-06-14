import pytest
import sys
import os

sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/..")

print (os.path)

print(__file__)
print (os.path.dirname(os.path.abspath(__file__)))

import Box2D as b2
# from Car import MovingCar,FreeCar
from Car import MovingCar,FreeCar


def InitFreeCar():
    # helper...
    world = b2.b2World()
    world.gravity=(0,0)
    freeCar = FreeCar(world,4,10)
    return (world,freeCar)


def test_FreeCar_instantiate():
    (world,car) = InitFreeCar()
    assert car != None



def test_FreeCar_still():
    # test if the car stands still
    (world,car) = InitFreeCar()
    timeStep = 0.01666
    p1 = car.GetPosition()
    for _ in range(100):
        world.Step(timeStep=timeStep,velocityIterations=1,positionIterations=1)
        car.Step(timeStep)
    p2 = car.GetPosition()
    d = p2-p1
    assert d.length < 0.001
 

def test_FreeCar_throttle():
    # test if the car is moving forward if throttled
    (world,car) = InitFreeCar()
    car.Throttle(1.0)   # full throttle !
    timeStep = 0.01666
    p1 = car.GetPosition()
    for _ in range(100):
        world.Step(timeStep=timeStep,velocityIterations=1,positionIterations=1)
        car.Step(timeStep)
    p2 = car.GetPosition()
    d = p2-p1
    assert d.length > 0.001


def test_FreeCar_turn_left():
    assert 0

def test_MovingCar_instantiate():
    world = b2.b2World()
    car = MovingCar(world,b2.b2Vec2(0,0),b2.b2Vec2(10,0),4,10)
    assert car != None
    
        

# test_FreeCar_still()        