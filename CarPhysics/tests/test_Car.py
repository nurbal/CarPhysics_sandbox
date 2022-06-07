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

def test_FreeCar_instantiate():
    world = b2.b2World()
    # freeCar = FreeCar(world,4,10)
    assert True


def test_MovingCar_instantiate():
    world = b2.b2World()
    # freeCar = FreeCar(world,4,10)
    assert 0
    
        