import Vec as vec
import random as rand

class Boid:
    def __init__(self, x, y, vx=3, vy=3, turn_speed=0.2):
        self.position = vec.Vec(x,y)
        self.velocity = vec.Vec(vx, vy)
        self.turn_factor = turn_speed

    def separate(self, boids):
        # returns a vector
        return vec.Vec(0, 0)

    def alignment(self, boids):
        # returns a vector
        return vec.Vec(0, 0)

    def cohesion(self, boids):
        # returns a vector
        return vec.Vec(0, 0)

    def next(self, boids):
        v1 = self.separate(boids)
        v2 = self.alignment(boids)
        v3 = self.cohesion(boids)

        self.velocity = self.velocity + v1 + v2 + v3
        self.position = self.position + self.velocity