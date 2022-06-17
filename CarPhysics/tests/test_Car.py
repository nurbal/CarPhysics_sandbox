import pytest
import sys
import os

sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/..")

print (os.path)


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



 
def test_FreeCar_inputValues():
    (world,car) = InitFreeCar()
    # these should not fail
    car.Throttle(-1)
    car.Throttle(0)
    car.Throttle(1)
    car.Break(0)
    car.Break(0.4238)
    car.Break(1)
    car.Turn(-1)
    car.Turn(0)
    car.Turn(1)
    # these should fail
    with pytest.raises(AssertionError):
        car.Throttle(-1.1)
    with pytest.raises(AssertionError):
        car.Throttle(1.1)
    with pytest.raises(AssertionError):
        car.Break(-0.1)
    with pytest.raises(AssertionError):
        car.Break(1.1)
    with pytest.raises(AssertionError):
        car.Turn(-1.1)
    with pytest.raises(AssertionError):
        car.Turn(1.1)



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
    assert p2.y - p1.y > 0.001

def test_FreeCar_reverse_throttle():
    # test if the car is moving forward if throttled
    (world,car) = InitFreeCar()
    car.Throttle(-1.0)   # full throttle !
    timeStep = 0.01666
    p1 = car.GetPosition()
    for _ in range(100):
        world.Step(timeStep=timeStep,velocityIterations=1,positionIterations=1)
        car.Step(timeStep)
    p2 = car.GetPosition()
    assert p2.y - p1.y < -0.001


def test_FreeCar_turn_right():
    # test if the car is moving slightly to the right
    (world,car) = InitFreeCar()
    car.Throttle(1.0)   # full throttle
    car.Turn(1.0)
    timeStep = 0.01666
    p1 = car.GetPosition()
    for _ in range(100):
        world.Step(timeStep=timeStep,velocityIterations=1,positionIterations=1)
        car.Step(timeStep)
    p2 = car.GetPosition()
    assert p2.x > p1.x

def test_MovingCar_instantiate():
    world = b2.b2World()
    car = MovingCar(world,b2.b2Vec2(0,0),b2.b2Vec2(10,0),4,10)
    assert car != None
    
        

# test_FreeCar_still()        