__author__ = 'Laxl'

import random
from euclid import Vector2
from math import sqrt

def length(v1, v2):
    return sqrt(((v1.x - v2.x)**2) + ((v1.y - v2.y)**2))

boid_colours = [(52, 117, 214), (215, 68, 52), (52, 216, 69), (200, 217, 52)]


class Boid():
    max_velocity = 500
    sight_range = 200
    proximity_value = 40

    def __init__(self, xpos, ypos):
        self.pos = Vector2(xpos, ypos)
        self.velocity = Vector2(0, 0)
        self.colour = random.choice(boid_colours)
        self.look_direction = Vector2(0, 0)

    def examine_flock(self, flock):
        #Returns the average perceived center, perceived direction and separation of Boids within sight_range
        v_sep, p_center, avg_dir = Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)
        # loop values
        neighbours = 0
        tot_pos, tot_dir = Vector2(0, 0), Vector2(0, 0)
        for b in flock:
            if b == self:
                continue
            dist = length(self.pos, b.pos)
            if dist < self.sight_range:
                if dist < self.proximity_value:  # This presumes sight range is never lower than prox value
                    v_sep -= (b.pos - self.pos)
                tot_pos += b.pos
                tot_dir += b.velocity
                neighbours += 1
        if neighbours > 0:
            p_center = tot_pos / neighbours
            avg_dir = tot_dir / neighbours
        return p_center, avg_dir, v_sep

    def bound_pos(self, dim):
        v = Vector2(0,0)
        x, y = self.pos.x, self.pos.y
        if x < 0:
            v.x = 10
        elif x > dim[0]:
            v.x = -10
        if y < 0:
            v.y = 10
        elif y > dim[1]:
            v.y = -10
        return v

    def goal(self, goal_packed):
        v_goal = Vector2(0, 0)
        if goal_packed[0]:
            goal_pos = goal_packed[0]
            attract = goal_packed[1]
            goal = Vector2(goal_pos[0], goal_pos[1])
            if length(goal, self.pos) < self.sight_range:
                attract_multiplier = 1 if attract else -1
                v_goal += attract_multiplier * ((goal - self.pos) / 4)
        return v_goal

    def is_max_velocity(self, velocity):
        return velocity.magnitude() > self.max_velocity

    def update_velocity(self, flock, goal, dim):
        p_center, p_direction, v_separation = self.examine_flock(flock)
        new_dir = Vector2(0, 0)
        #Rules
        v1 = (p_center - self.pos) / 100        # Boid steers toward perceived center of flock
        v2 = v_separation                       # Boid tries to separate from nearby flock mates
        v3 = (p_direction - self.velocity) / 8  # Boid aligns to perceived flock direction
        v4 = self.bound_pos(dim)                # Boid steers away from edges of environment(screen)
        new_dir += v1 + v2 + v3 + v4
        if goal[0]:
            v5 = self.goal(goal)                #Boid steers toward/away from goal(mouse)
            new_dir += v5
        self.velocity += new_dir

        linear_velocity = self.velocity.magnitude()
        #If Boid is given no velocity from any rules, it is given a random speed. Only happens before they form flocks
        if linear_velocity == 0:
            self.velocity = Vector2(random.uniform(-1,1), random.uniform(-1, 1)) * self.max_velocity
        if self.is_max_velocity(self.velocity):
            self.velocity = (self.velocity/linear_velocity) * self.max_velocity

        #This is only to get a point in front of boids position to draw the 'beak'
        if linear_velocity > 0:
            self.look_direction = (self.velocity / linear_velocity) * 20

    def update_position(self, dt):
        self.pos += self.velocity * dt

    def update(self, flock, goal, dim, dt):
        self.update_velocity(flock, goal, dim)
        self.update_position(dt)


class FlockController():
    def __init__(self, width, height, amt):
        self.width, self.height = width, height  # max width height of environment
        self.flock = self.initialize_boids(amt)

    def initialize_boids(self, amt):
        flock = []
        for i in range(0, amt):
            flock.append(Boid(random.randint(0, self.width), random.randint(0, self.height)))
        return flock

    def move_flock(self, goal, dt):
        for b in self.flock:
            b.update(self.flock, goal, (self.width, self.height), dt)

    def update(self, goal, dt):
        self.move_flock(goal, dt)
