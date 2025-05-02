import Vec as vec

max_speed = 5
class Boid:
    def __init__(self, x, y, vx=3, vy=3, turn_speed=0.5):
        self.position = vec.Vec(x,y)        # Position as a vector
        self.velocity = vec.Vec(vx, vy)     # Velocity as a vector
        self.turn_factor = turn_speed

    def separation(self, boids):
        desired_separation = 2.0
        steer = vec.Vec(0, 0)
        #diff = vec.Vec(0, 0)
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < desired_separation:
                    diff = self.position - boid.position
                    diff.normalize()
                    diff /= dist
                    steer += diff
                    count += 1

        if count > 0:
            steer /= count
        if steer.magnitude() > 0:
            steer.normalize()
            steer *= self.turn_factor
            #steer -= self.velocity
            steer.limit(self.turn_factor)
            return steer
        else:
            return steer

    def alignment(self, boids):
        prefer_distance = 5.0
        velo_sum = vec.Vec(0, 0)
        steer = vec.Vec(0, 0)
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < prefer_distance:
                    velo_sum += boid.velocity
                    count += 1

        if count > 0:
            avg = velo_sum / count
            avg.normalize()
            avg *= self.turn_factor
            steer = avg - self.velocity
            steer.limit(self.turn_factor)
            return steer
        else:
            return steer

    def cohesion(self, boids):
        visible_distance = 7.5
        center = vec.Vec(0, 0)
        visible_positions = vec.Vec(0, 0)
        steer = vec.Vec(0, 0)
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < visible_distance:
                    visible_positions += boid.position
                    count += 1

        if count > 0:
            center = (visible_positions / count)
            desired = center - self.position
            desired.normalize()
            desired *= self.turn_factor
            steer.limit(self.turn_factor)
            return steer
        else:
            return steer

    def avoid_walls(self, width, height, margin):
        steer = vec.Vec(0, 0)
        if self.position.x < margin:
            steer.x = self.turn_factor
        if self.position.x > width - margin:
            steer.x = -self.turn_factor
        if self.position.y < margin:
            steer.y = self.turn_factor
        if self.position.y > height - margin:
            steer.y = -self.turn_factor
        return steer


    def next(self, boids, width, height, margin=50):
        s_f = self.separation(boids)
        a_f = self.alignment(boids)
        c_f = self.cohesion(boids)
        a_w_f = vec.Vec(0, 0)
        if width and height:
            a_w_f = self.avoid_walls(self.position.x, self.position.y, margin)

        self.velocity += s_f + a_f + c_f + a_w_f
        self.velocity.limit(max_speed)
        self.position += self.velocity