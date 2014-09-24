__author__ = 'Laxl'

import numpy as np
import random

boid_colours = [(52, 117, 214), (215, 68, 52), (52, 216, 69), (200, 217, 52)]

class Boid():
    max_velocity = 400
    sight_range = 300
    proximity_value = 80

    def __init__(self, xpos, ypos):
        self.pos = np.array([xpos, ypos])
        self.velocity = np.array([0, 0])
        self.colour = random.choice(boid_colours)
        self.look_direction = np.array([0, 0])

    def perceived_center_pos_direction(self, flock):
        tot_pos = np.array([0,0])
        tot_dir = np.array([0, 0])
        v_sep = np.array([0, 0])
        neighbours = 0
        for b in flock:
            if b == self:
                continue
            dist = np.linalg.norm(self.pos - b.pos)
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
        v = np.array([0,0])
        x = self.pos[0]
        y = self.pos[1]
        if x < dim[0]/4:
            v[0] = 10
        elif x > (dim[0]/4)*3:
            v[0] = -10
        if y < dim[1]/4:
            v[1] = 10
        elif y > (dim[1]/4)*3:
            v[1] = -10
        return v

    def goal(self, goal_pos):
        goal = np.array([goal_pos[0], goal_pos[1]])
        if np.linalg.norm(goal - self.pos) < self.sight_range:
            return (goal - self.pos)
        return np.array([0, 0])

    def update_velocity(self, flock, goal, dim):
        p_center, p_direction, v_separation = self.perceived_center_pos_direction(flock)
        # if p_center == None and p_direction == None and v_separation == None:
        #     print "random speed!"
        #     vx = np.array([random.uniform(0,1), random.uniform(0, 1)]) * random.randint (100, self.max_velocity)
        # else:
        #     vx = np.array([0, 0])

        if p_center != None:
            v1 = (p_center - self.pos) / 20
        else:
            v1 = np.array([0,0])

        if v_separation != None:
            v2 = v_separation / 6
        else:
            v2 = np.array([0, 0])

        if p_direction != None:
            v3 = (p_direction - self.velocity) / 8
        else:
            v3 = np.array([0,0])
        #v4 = self.bound_pos(dim)
        if goal:
            v5 = self.goal(goal)
        else:
            v5 = np.array([0,0])
        #print v1, v2, v3, v4
        self.velocity += v1 + v2 + v3 +v5
        linear_velocity = np.linalg.norm(self.velocity)
        if linear_velocity == 0:
            self.velocity = np.array([random.uniform(0,1), random.uniform(0, 1)]) * random.randint (-self.max_velocity, self.max_velocity)
        if linear_velocity > self.max_velocity:
            self.velocity = (self.velocity/linear_velocity) * self.max_velocity

        #This is only to get a point in front of boids position to draw 'beak'
        if linear_velocity > 0:
            self.look_direction = (self.velocity / linear_velocity) * 20

    def update_position(self, dim, dt):
        self.pos += self.velocity *dt
        self.pos[0] %= dim[0]
        self.pos[1] %= dim[1]

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


# class Vector2(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def __add__(self, other):
#         if type(other) != type(self):
#             raise ValueError
#         else:
#             self.x += other.x
#             self.y += other.y
#
#     def __sub__(self, other):
#         if type(other) != type(self):
#             raise ValueError
#         else:
#             self.x -= other.x
#             self.y -= other.y
#
#     def __mul__(self, other):
#         self.x *= other
#         self.y *= other
#
#     def __div__(self, other):
#         self.x /= other
#         self.y /= other
#
#     def __str__(self):
#         return "[%d, %d]" % (self.x, self.y)