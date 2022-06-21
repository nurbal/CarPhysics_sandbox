import random as rd
import Box2D as b2
import math
# import sys
# import os
# sys.path.insert(0, f"{os.path.dirname(os.path.abspath(__file__))}")
# import WayPoints

class BaseCar:
    def __init__(self):
        pass

    def GetPosition(self):
        return b2.b2Vec2(self.body.position)
        # return self.body.position

    
# Free Car (the one controller manually)
class FreeCar(BaseCar) :
    def __init__(self,world,spawnDistance,maxDistance):
        self.world = world

        # temporarily set a maximum distance to trigger a respawn at (0,0)
        self.spawnDistance = spawnDistance
        self.maxDistance = maxDistance

        # vehicle characteristics
        self.maxSpeed = 10          # m/s
        self.maxReverseSpeed = -1          # m/s
        self.maxThrottleAccel = 5   # m.s-2
        self.maxThrottleReverseAccel = 1   # m.s-2
        self.maxBreakAccel = 20     # m.s-2
        self.minTurnRadius = 5      # m

        # vehicle status
        # TODO make them properties !
        self.throttleAccel = 0   # [-1..1]
        self.breakAccel = 0     # [0..1]
        self.steeringValue = 0   # [-1..1] -1=left, 1=right, 0=center
        self.speed = 0.0


        carShape = b2.b2PolygonShape(box=(1,2))
        boxFD = b2.b2FixtureDef(
            shape=carShape,
            friction=0.2,
            density=20,
        )
        self.body = self.world.CreateDynamicBody(
            position=(
                rd.uniform(-self.spawnDistance,self.spawnDistance),
                rd.uniform(-self.spawnDistance,self.spawnDistance),
            ),
            fixtures=boxFD,
        )
        # TODO: orienter le body selon self.direction

    def Step(self,timeStep):
        # respawn if too far from origin
        if self.body.position.length > self.maxDistance :
            self.body.position = (
                rd.uniform(-self.spawnDistance,self.spawnDistance),
                rd.uniform(-self.spawnDistance,self.spawnDistance),
            )
        # compute accelerations
        speedTarget = 0.0
        acceleration = 0.0
        if self.throttleAccel > 0:
            if self.throttleAccel > self.breakAccel:  # accel forward
                speedTarget = self.maxSpeed
                acceleration = self.throttleAccel - self.breakAccel
            else:    # break
                speedTarget = 0.0
                acceleration = self.breakAccel - self.throttleAccel   
        else:
            if self.throttleAccel < -self.breakAccel:  # accel forward
                speedTarget = self.maxReverseSpeed
                acceleration = abs(self.throttleAccel) - self.breakAccel
            else:    # break
                speedTarget = 0.0
                acceleration = self.breakAccel - abs(self.throttleAccel)
        # compute speed
        deltaV = acceleration * timeStep
        if self.speed < speedTarget:
            self.speed = min(self.speed+deltaV,speedTarget)
        else:
            self.speed = max(self.speed-deltaV,speedTarget)
        # move
        c = math.cos(self.body.angle)
        s = math.sin(self.body.angle)
        forward = b2.b2Vec2(-s,c)   # Y axis=forward, X=right
        right = b2.b2Vec2(c,s)

        dP = self.speed*timeStep    # abscisse curviligne
        (dx,dy) = (0,dP)    # default forward values
        if abs(self.steeringValue)>0.01:
            # we are turning
            ray = 1.0/self.steeringValue * self.minTurnRadius
            alpha = dP/ray
            dx = -ray*(1.0-math.cos(alpha))
            dy = ray*math.sin(alpha)
            self.body.angle = self.body.angle - alpha
        self.body.position = self.body.position + dx*right + dy*forward
        
           
        

    def Throttle(self,value):
        assert value>=-1 and value <=1
        if value>0:
            self.throttleAccel = value * self.maxThrottleAccel
        else:
            self.throttleAccel = value * self.maxThrottleReverseAccel
        self.breakAccel = 0 # could be matter of design discussion ?

    def Break(self,value):
        assert value>=0 and value <=1
        self.breakAccel = value * self.maxBreakAccel
        self.throttleValue = 0 # could be matter of design discussion ?

    def Turn(self,value):
        assert value>=-1 and value <=1
        self.steeringValue = value





# moving car (straight line, from A to B and back again)
class MovingCar(BaseCar) :
    def __init__(self,world,initialpos,endpos,speed,initialtrip=0.0):
        self.initialpos = b2.b2Vec2(initialpos)
        self.direction = b2.b2Vec2(endpos) - self.initialpos
        self.tripLen = self.direction.Normalize()
        self.speed = speed
        self.trip = initialtrip
        self.world = world

        carShape = b2.b2PolygonShape(box=(1,1))
        boxFD = b2.b2FixtureDef(
            shape=carShape,
            friction=0.2,
            density=20,
        )
        self.body = self.world.CreateBody(
            position=self.initialpos,
            fixtures=boxFD,
        )
        # TODO: orienter le body selon self.direction

    def Step(self,timeStep):
        self.trip += self.speed * timeStep
        if self.trip > self.tripLen:
            self.trip = 0.0
        self.body.position = self.initialpos + (self.direction * self.trip)
        self.body.linearVelocity = self.direction*self.speed
        self.body.angularVelocity = 0.0

# a car following a waypoints trajectory
class WaypointsCar(BaseCar):
    def __init__(self,world,trajectory,speed,initialtrip=0):
        self.trajectory = trajectory
        self.speed = speed
        self.trip = initialtrip
        self.world = world

        (position,angle)=self.trajectory.GetPositionAngle(initialtrip)

        carShape = b2.b2PolygonShape(box=(2,1))
        boxFD = b2.b2FixtureDef(
            shape=carShape,
            friction=0.2,
            density=20,
        )
        self.body = self.world.CreateBody(
            position=position,
            angle=angle,
            fixtures=boxFD,
        )
    
    def Step(self,timeStep):
        self.trip = (self.trip + self.speed * timeStep) % self.trajectory.length
        (self.body.position,self.body.angle) = self.trajectory.GetPositionAngle(self.trip)
        # TODO velocities
        


