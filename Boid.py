import Vec as vec

max_speed = 10
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
        #self.fatigue_level = "rested"
        #self.fatigue_count = 0

    '''
    Fatigue ideas:
    - This would make it a 5th force in the algorithm, would be added to the velocity in next() method. Up to
    other ideas and interpretations of this, though. This is just my first idea.
    - Fatigue levels: rested, tired, fatigued.
    - Fatigue count: time the boid has been in each level, probably using a timer or by frame or update count.
    - This specific idea would make all boids fatigued at the same time and same rate, which is fine, but not exactly
    what Dutter gave us as an idea. Might not be really what we wanted as our main goal. Should really talk about this.
    
    JAMES: I like this idea ^. I think something we could try is making the fatigue count inversely proportional to
    the # of neighbors. So the more boids are nearby, the less they get fatigued. Something to note w/ this is that
    it might affect boids on the outside the same way no matter if they are in front or not, so we might want a new
    check for neighbors in front of any boid in cohesion(). Then that could be our value. Then while in the fatigued
    state, we could slowly reduce their fatigue as long as enough boids are nearby. Idk what an elegant way to have
    the boid move towards the middle of the flock would be though.
    
    - Could maybe do the state machine in Main instead to calculate things? Making this a state machine makes it
    harder for me to see the best way to do it.
    
    - If we want to just do it to the leader of a group, could maybe calculate the boid furthest away from the center 
    of mass we calculate in cohesion() method. This could be flawed though and lead to inaccurate results, and it would
    be hard to figure out, though probably not impossible considering the time we have left.
    '''
    def fatigue(self):
        pass

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
                if 0 < dist < desired_separation:
                    diff = (self.position - boid.position).normalize()
                    diff /= dist
                    steer += diff
                    count += 1

        if count > 0:
            steer /= count
            if steer.magnitude() > 0:
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
                if 0 < dist < prefer_distance:
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
                if 0 < dist < visible_distance:
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

        steer = s_f * 1.5 + a_f * 1.0 + c_f * 1.0 + a_w_f * 2.0
        steer.limit(self.turn_factor)

        # Direct add
        new_velocity = self.velocity + steer
        self.velocity = self.velocity.linear_interpolate(new_velocity, 0.1) #Interpolation with 10% blend (NEEDS APPROVAL)
        self.velocity.limit(max_speed)
        self.position += self.velocity

        '''
        JAMES: Plugged in the linear interpolation that you outlined (needs to be approved) but 
        even with this the speed still shifts wildly and is lost over time as boids align with others. 
        I'm sure there is an elegant way to fix this but I haven't figured it out yet.
        '''