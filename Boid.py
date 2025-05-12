import Vec as vec
import math

max_speed = 3
min_speed = 1
class Boid:
    """
    Class for a Boid object, the main object in the simulation.
    Defines all behaviors of the boid according to the algorithm.
    """
    def __init__(self, x, y, vx, vy, turn_factor=1.2):
        """
        Constructor for a Boid object. Represents position and velocity as 2D vectors.
        :param x: X position.
        :param y: Y position.
        :param vx: X velocity.
        :param vy: Y velocity.
        :param turn_factor: Turn speed of the Boid object.
        """
        self.position = vec.Vec(x,y)        # Position as a vector
        self.velocity = vec.Vec(vx, vy)     # Velocity as a vector
        self.turn_factor = turn_factor
        self.fatigue = 0.0
        self.max_fatigue = 50.0
        self.fatigue_rate = 0.5

    def can_see(self, other, angle=(math.radians(120))):
        direction = other.position - self.position
        return vec.Vec.angleBetween(direction, self.velocity) <= angle

    def fatigue_force(self, boids):
        """
        Method for fatigue.
        Boids will slow down (be fatigued) if they are not seeing other boids.
        If they are seeing other boids, they will speed up again.
        :param boids: List of Boid objects.
        :return: Force vector, to be added to the velocity.
        """
        visible_distance = 50
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < visible_distance and self.can_see(boid):
                    count += 1

        if count < 4:
            self.fatigue += (4 - count) * self.fatigue_rate
        else:
            self.fatigue -= (count - 4) * self.fatigue_rate

        self.fatigue = max(0.0, min(self.fatigue, self.max_fatigue))
        force = self.velocity.normalize() * -0.03 * self.fatigue
        return force

    def separation(self, boids):
        """
        Method for separation.
        Boids will steer away from other boids within the desired distance.
        :param boids: List of Boid objects.
        :return: Steer vector, to be added to the velocity.
        """
        desired_separation = 20     # 20 is the sweet spot
        steer = vec.Vec(0, 0)
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < desired_separation and self.can_see(boid):
                    diff = (self.position - boid.position).normalize()
                    diff /= dist
                    steer += diff
                    count += 1

        if count > 0:
            steer /= count
            steer.normalize()
            steer *= self.turn_factor
        return steer

    def alignment(self, boids):
        """
        Method for alignment.
        Boids will steer towards the average velocity of the group of boids, within the preferred distance.
        :param boids: List of Boid objects.
        :return: Steer vector, to be added to the velocity.
        """
        prefer_distance = 25
        avg_vel = vec.Vec(0, 0)
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < prefer_distance and self.can_see(boid):
                    avg_vel += boid.velocity
                    count += 1

        if count > 0:
            avg_vel /= count
            avg_vel.normalize()
            avg_vel *= self.turn_factor
            steer = avg_vel - self.velocity
            return steer
        return vec.Vec(0, 0)

    def cohesion(self, boids):
        """
        Method for cohesion.
        Boids will steer towards the center of the group of boids, within the visible distance.
        :param boids: List of Boid objects.
        :return: Desired steer vector, to be added to the velocity.
        """
        visible_distance = 25
        center = vec.Vec(0, 0)
        count = 0
        for boid in boids:
            if boid is not self:
                dist = vec.Vec.distance(self.position, boid.position)
                if 0 < dist < visible_distance and self.can_see(boid):
                    center += boid.position
                    count += 1

        if count > 0:
            center /= count
            desired = (center - self.position).normalize()
            desired *= self.turn_factor
            return desired
        return vec.Vec(0, 0)

    def avoid_walls(self, width, height, margin=20):
        """
        Method for avoiding walls.
        :param width: Width of the window.
        :param height: Height of the window.
        :param margin: Margin for avoiding walls.
        :return: Steer vector to be added to the velocity.
        """
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

    def next(self, boids, width, height):
        """
        Method for updating the Boid object's position and velocity.
        :param boids: List of Boid objects.
        :param width: Width of the window.
        :param height: Height of the window.
        :return: Boid's position added to its new velocity.
        """
        s_f = self.separation(boids)
        a_f = self.alignment(boids)
        c_f = self.cohesion(boids)
        a_w_f = vec.Vec(0, 0)
        if width and height:
            a_w_f = self.avoid_walls(width, height)
        f_f = self.fatigue_force(boids)

        steer = s_f * 1.5 + a_f * 1.3 + c_f * 1.3 + a_w_f * 2.0 + f_f
        steer.limit(self.turn_factor)

        new_vel = self.velocity + steer
        self.velocity = self.velocity.linear_interpolate(new_vel, 0.45)
        self.velocity *= 2      # Artificial increase, needed for Boids to actually have a decent speed
        self.velocity.limit(max_speed)
        self.velocity.bottom_limit(min_speed)
        self.position += self.velocity