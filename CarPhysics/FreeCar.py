from random import uniform
from Box2D import * 

class FreeCar :
    def __init__(self,world,spawnDistance,maxDistance):
        self.world = world
        self.spawnDistance = spawnDistance
        self.maxDistance = maxDistance

        carShape = b2PolygonShape(box=(1,2))
        boxFD = b2FixtureDef(
            shape=carShape,
            friction=0.2,
            density=20,
        )
        self.body = self.world.CreateDynamicBody(
            position=(
                uniform(-self.spawnDistance,self.spawnDistance),
                uniform(-self.spawnDistance,self.spawnDistance),
            ),
            fixtures=boxFD,
        )
        # TODO: orienter le body selon self.direction

    def Step(self,timeStep):
        if self.body.position.length > self.maxDistance :
            self.body.position = (
                uniform(-self.spawnDistance,self.spawnDistance),
                uniform(-self.spawnDistance,self.spawnDistance),
            )
        return

    def Throttle(self,value):
        pass
    def Break(self,value):
        pass
    def Turn(self,value):
        pass
