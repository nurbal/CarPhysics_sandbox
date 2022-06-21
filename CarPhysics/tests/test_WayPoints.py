import pytest
import sys
import os
import math

sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}/..")
from Box2D import b2Vec2
from WayPoints import Trajectory

def InitTriangularTrajectory():
    # triangle rectangle de côtés 3,4,5
    A = b2Vec2(0,0)
    B = b2Vec2(4,0)
    C = b2Vec2(0,3)
    return Trajectory([A,B,C,A])

def test_Trajectory_Length():
    t = InitTriangularTrajectory()
    assert abs(t.length-12)<0.00001

def test_Trajectory_NbSegments():
    t = InitTriangularTrajectory()
    assert t.nbSegments == 3

def test_Trajectory_SegmentsLen():
    t = InitTriangularTrajectory()
    assert abs(t.segments[0].length-4) < 0.0001
    assert abs(t.segments[1].length-5) < 0.0001
    assert abs(t.segments[2].length-3) < 0.0001

def test_Trajectory_SegmentsAbscissa():
    t = InitTriangularTrajectory()
    assert abs(t.segmentsAbscissa[0]-0) < 0.0001
    assert abs(t.segmentsAbscissa[1]-4) < 0.0001
    assert abs(t.segmentsAbscissa[2]-9) < 0.0001

def test_Trajectory_GetPosition():
    t = InitTriangularTrajectory()
    (position,angle) = t.GetPositionAngle(1) # get position and angle at abscissa 1.0
    assert (position-b2Vec2(1,0)).length < 0.0001
    assert abs(angle) < 0.0001
    (position,angle) = t.GetPositionAngle(10) # get position and angle at abscissa 1.0
    assert (position-b2Vec2(0,2)).length < 0.0001
    assert abs(angle+math.pi/2) < 0.0001