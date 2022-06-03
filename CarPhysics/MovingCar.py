# from BaseCar import *
from Box2D import b2Vec2,b2PolygonShape,b2FixtureDef

# moving car (no free move)
class MovingCar() :
    def __init__(self,world,initialpos,endpos,speed,initialtrip=0.0):
        self.initialpos = b2Vec2(initialpos)
        self.direction = b2Vec2(endpos) - self.initialpos
        self.tripLen = self.direction.Normalize()
        self.speed = speed
        self.trip = initialtrip
        self.world = world

        carShape = b2PolygonShape(box=(1,1))
        boxFD = b2FixtureDef(
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
