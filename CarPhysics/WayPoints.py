# trajectories and waypoints
# very simple trajectory system, made of a vector of waypoints...

from cmath import atan
from Box2D import b2Vec2
from jinja2 import pass_context


import math

def GetVec2Angle(v):
    assert abs(v.length-1) < 0.0001
    angle = math.acos(v.x)
    if v.y<0:
        angle =-angle
    return angle


# a waypoint is simply a b2Vec2

class Trajectory:
    def __init__(self,waypoints):
        assert len(waypoints) > 1
        self._waypoints = []
        for p in waypoints:
            self._waypoints.append (b2Vec2(p))
        prev_p = self._waypoints[0]
        self._segments = []
        self._segmentsLengths = []       # length of a given segment
        self._segmentsAbscissa = []  # abscissa of the start of the segment
        self._segmentsDirection = []    # unit vectors
        totalLength = 0
        for p in self._waypoints[1:]:
            segment = p - prev_p
            prev_p = p
            l = segment.length
            self._segments.append(segment)
            self._segmentsLengths.append(l)
            self._segmentsAbscissa.append(totalLength)
            self._segmentsDirection.append(segment / l)
            totalLength += l
            
    @property
    def length(self):
        total = 0;
        for l in self._segmentsLengths:
            total += l
        return total

    @property
    def nbSegments(self):
        return len(self._segments)

    @property
    def segments(self):
        return self._segments

    @property
    def segmentsAbscissa(self):
        return self._segmentsAbscissa

    @property
    def waypoints(self):
        return self._waypoints

    # get a position and an angle, at a specific abscissa of the trajectory
    def GetPositionAngle(self,abscissa):
        x = abscissa%self.length
        for i in range(len(self._segments)):
            if self._segmentsAbscissa[i]+self._segmentsLengths[i]>=x:
                # here we are, on the right segment of trajectory
                position = self._waypoints[i]+self._segmentsDirection[i]*(x-self._segmentsAbscissa[i])
                angle = GetVec2Angle(self._segmentsDirection[i])
                return (position,angle)

        



    
# class TrajectoryIterator:
