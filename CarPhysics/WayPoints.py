# trajectories and waypoints
# very simple trajectory system, made of a vector of waypoints...

from Box2D import b2Vec2
from jinja2 import pass_context

# a waypoint is simply a b2Vec2

class Trajectory:
    def __init__(self,waypoints):
        assert len(waypoints) > 1
        self._waypoints = waypoints
        prev_p = self._waypoints[0]
        self._segments = []
        self._segmentsLengths = []       # length of a given segment
        self._segmentsAbscissa = []  # abscissa of the start of the segment
        totalLength = 0
        for p in self._waypoints[1:]:
            segment = p - prev_p
            prev_p = p
            self._segments.append(segment)
            self._segmentsLengths.append(segment.length)
            self._segmentsAbscissa.append(totalLength)
            totalLength += segment.length
    
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
    



    
# class TrajectoryIterator:
