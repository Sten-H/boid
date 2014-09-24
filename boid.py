__author__ = 'Laxl'

import random
from euclid import Vector2
from math import sqrt

def length(v1):
    return sqrt(Vector2.magnitude_squared(v1))

boid_colours = [(52, 117, 214), (215, 68, 52), (52, 216, 69), (200, 217, 52)]

class Boid():
    max_velocity = 500
    sight_range = 150
    proximity_value = 40

    def __init__(self, xpos, ypos):
        self.pos = Vector2(xpos, ypos)
        self.velocity = Vector2(0, 0)
        self.colour = random.choice(boid_colours)
        self.look_direction = Vector2(0, 0)

    def perceived_center_pos_direction(self, flock):
        tot_pos = Vector2(0, 0)
        tot_dir = Vector2(0, 0)
        v_sep = Vector2(0, 0)
        neighbours = 0
        for b in flock:
            if b == self:
                continue
            dist = length(self.pos - b.pos)
            if dist < self.proximity_value:
                v_sep -= (b.pos - self.pos)
            if dist < self.sight_range:
                tot_pos += b.pos
                tot_dir += b.velocity
                neighbours += 1
        if neighbours > 0:
            p_center = tot_pos / neighbours
            avg_dir = tot_dir / neighbours
            return p_center, avg_dir, v_sep
        return None, None, v_sep

    def bound_pos(self, dim):
        v = Vector2(0,0)
        x = self.pos.x
        y = self.pos.y
        if x < dim[0]/4:
            v.x = 10
        elif x > (dim[0]/4)*3:
            v.x = -10
        if y < dim[1]/4:
            v.y = 10
        elif y > (dim[1]/4)*3:
            v.y = -10
        return v

    def goal(self, goal_pos):
        goal = Vector2(goal_pos[0][0], goal_pos[0][1])
        attractive = goal_pos[1]
        mult = 0
        if attractive == True:
            mult = 1
        else:
            mult = -1
        if length(goal - self.pos) < self.sight_range:
            return mult*((goal - self.pos) / 4)
        return Vector2(0, 0)

    def update_velocity(self, flock, goal, dim):
        p_center, p_direction, v_separation = self.perceived_center_pos_direction(flock)

        if p_center:
            v1 = (p_center - self.pos) / 100
        else:
            v1 = Vector2(0, 0)

        v2 = v_separation

        if p_direction:
            v3 = (p_direction - self.velocity) / 8
        else:
            v3 = Vector2(0, 0)
        v4 = self.bound_pos(dim)
        if goal[0]:
            v5 = self.goal(goal)
        else:
            v5 = Vector2(0, 0)
        self.velocity += v1 + v2 + v3 + v4 + v5
        linear_velocity = length(self.velocity)
        if linear_velocity == 0:
            self.velocity = Vector2(random.uniform(-1,1), random.uniform(-1, 1)) * random.randint(self.max_velocity*0.7, self.max_velocity)
        if linear_velocity > self.max_velocity:
            self.velocity = (self.velocity/linear_velocity) * self.max_velocity

        #This is only to get a point in front of boids position to draw 'beak'
        if linear_velocity > 0:
            self.look_direction = (self.velocity / linear_velocity) * 20

    def update_position(self, dim, dt):
        self.pos += self.velocity * dt
        #wrap around screen
        #self.pos.x %= dim[0]
        #self.pos.y %= dim[1]

    def update(self, flock, goal, dim, dt):
        self.update_velocity(flock, goal, dim)
        self.update_position(dim, dt)


class FlockController():
    def __init__(self, width, height, amt):
        self.width, self.height = width, height  # max width height of environment
        self.flock = self.initialize_boids(amt)

    def initialize_boids(self, amt):
        flock = []
        for i in range(0, amt):
            flock.append(Boid(random.randint(0, self.width), random.randint(0, self.height)))
        # return list of created boids with randomised positions
        return flock

    def move_flock(self, goal, dt):
        for b in self.flock:
            b.update(self.flock, goal, (self.width, self.height), dt)

    def update(self, goal, dt):
        self.move_flock(goal, dt)
