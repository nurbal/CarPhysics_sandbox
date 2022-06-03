import random as rd
import Box2D as b2



class BaseCar:
    def __init__(self):
        pass

    
# Free Car (the one controller manually)
class FreeCar(BaseCar) :
    def __init__(self,world,spawnDistance,maxDistance):
        self.world = world
        self.spawnDistance = spawnDistance
        self.maxDistance = maxDistance

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
        if self.body.position.length > self.maxDistance :
            self.body.position = (
                rd.uniform(-self.spawnDistance,self.spawnDistance),
                rd.uniform(-self.spawnDistance,self.spawnDistance),
            )
        return

    def Throttle(self,value):
        pass
    def Break(self,value):
        pass
    def Turn(self,value):
        pass





# moving car (no free move)
class MovingCar() :
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
