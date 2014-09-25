__author__ = 'Laxl'

import random
from euclid import Vector2
from math import sqrt
from math import pow


    #return (v1-v2).magnitude()


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

    def __str__(self):
        return str(self.pos)
    def __repr__(self):
        return self.__str__()

    def length(self, v1, v2):
        x1, x2, y1, y2 = v1.x, v2.x, v1.y, v2.y
        return sqrt(pow((x1 - x2),2) + pow((y1 - y2), 2))

    def examine_boid(self, b, v):
        if b == self:
            return
        dist = self.length(self.pos, b.pos)
        if dist < self.proximity_value:
            v[2] -= (b.pos - self.pos)
        if dist < self.sight_range:
            v[0] += b.pos
            v[1] += b.velocity
            v[3] += 1

    def examine_flock(self, flock):
        #Returns the average perceived center, perceived direction and separation of Boids within sight_range
        #v_sep, p_center, avg_dir = Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)
        # loop values
        vectors = [Vector2(0,0), Vector2(0, 0), Vector2(0, 0), 0]
        [self.examine_boid(b, vectors) for b in flock]
        #map(self.examine_boid, flock)
        p_center, avg_dir, v_sep = vectors[0], vectors[1], vectors[2]
        neighbours = vectors[3]
        if neighbours > 0:
            p_center = p_center / neighbours
            avg_dir = avg_dir / neighbours
        return p_center, avg_dir, v_sep

    def bound_pos(self, dim):
        bound_multiplier = 2
        v = Vector2(0, 0)
        x, y = self.pos.x, self.pos.y
        if x < 0:
            v.x = 10
        elif x > dim[0]:
            v.x = -10
        if y < 0:
            v.y = 10
        elif y > dim[1]:
            v.y = -10
        return v * bound_multiplier

    def goal(self, goal_packed):
        v_goal = Vector2(0, 0)
        if goal_packed[0]:
            goal_pos = goal_packed[0]
            attract = goal_packed[1]
            goal = Vector2(goal_pos[0], goal_pos[1])
            if self.length(goal, self.pos) < self.sight_range:
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
        elif self.is_max_velocity(self.velocity):
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
        self.swarm_grid = SwarmGrid(width, height)
        self.flock = self.initialize_boids(amt)
        self.swarm_grid.populate(self.flock)

    def initialize_boids(self, amt):
        flock = []
        for i in range(0, amt):
            b = Boid(random.randint(0, self.width), random.randint(0, self.height))
            flock.append(b)
        return flock

    def move_flock(self, goal, dt):
        for b in self.flock:
            local_swarm = self.swarm_grid.get_neighbourhood(b)
            b.update(local_swarm, goal, (self.width, self.height), dt)

    def update(self, goal, dt):
        self.move_flock(goal, dt)
        self.swarm_grid.update_grid()


class SwarmGrid():
    cell_size = 100
    boids = []
    def __init__(self, width, height):
        x_cells = width // self.cell_size
        y_cells = height // self.cell_size
        self.x_max_width = int((x_cells - 1) * 1.2)
        self.x_min_width = int(0 -(self.x_max_width * 0.2))
        self.y_max_width = int((y_cells - 1) * 1.2)
        self.y_min_width = int(0 -(self.y_max_width * 0.2))
        self.cell_map = {}
        self.search_range = self.cell_size
        for x in range(self.x_min_width, self.x_max_width+1):
            for y in range(self.y_min_width, self.y_max_width+1):
                self.cell_map[(x,y)] = []

    def populate(self, flock):
        [self.add(b) for b in flock]

    def cell_id(self,x_pos, y_pos):
        x, y = x_pos//self.search_range, y_pos//self.search_range
        #Store negative values in 0 cell
        x = max(self.x_min_width, x)
        x = min(x, self.x_max_width)
        y = max(self.y_min_width, y)
        y = min(y, self.y_max_width)
        print x,y
        return x,y

    def add(self, b):
        self.boids.append(b)
        self._put_in_grid(b)

    def _put_in_grid(self, b):
        self.cell_map[self.cell_id(b.pos.x, b.pos.y)].append(b)

    def get_neighbourhood(self, b):
        neighbourhood = []
        x, y = self.cell_id(b.pos.x, b.pos.y)
        for i in range(-1,2):
            for j in range(-1, 2):
                new_x = x + i
                new_y = y + j
                new_x = max(new_x, 0)
                new_x = min(new_x, self.x_max_width)
                new_y = max(new_y, 0)
                new_y = min(new_y, self.y_max_width)
                neighbourhood += self.cell_map[(new_x, new_y)]
        return neighbourhood

    def update_grid(self):
        for c in self.cell_map.values():
            c[:] = []
        [self._put_in_grid(b) for b in self.boids]


