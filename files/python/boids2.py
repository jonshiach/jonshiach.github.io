#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:11:47 2022

@author: jon
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, collections

def Norm(x, y):
    return np.sqrt(x ** 2 + y ** 2)


def Distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def Limit(x, y, lower, upper):
    norm = Norm(x, y)
    if norm < lower:
        x = x / norm * lower
        y = y / norm * lower
    elif norm > upper:
        x = x / norm * upper
        y = y / norm * upper
        
    return x, y


class boid:
    
    def __init__(self):
        self.x = width * np.random.rand()   # x co-ordinate
        self.y = height * np.random.rand()  # y co-ordinate
        self.u = np.random.uniform(-1, 1)   # velocity in the x direction
        self.v = np.random.uniform(-1, 1)   # velocity in the y direction
        self.sx = 0                         # steering force in the x direction
        self.sy = 0                         # steering force in the y direction
        self.minspeed = 5                   # minimum speed of the agent
        self.maxspeed = 10                  # maximum speed of the agent
        self.neighbours = []                # list of neighbouring agents
        self.u, self.v = Limit(self.u, self.v, self.maxspeed, self.maxspeed)
       

    def Neighbours(self, boidList):
        self.neighbours = []
        for neighbour in boidList: 
            if id(self) == id(neighbour):
                continue
            d = Distance(self.x, self.y, neighbour.x, neighbour.y)
            if d < detection_radius:
                self.neighbours.append(neighbour)
                    
                    
    def Move(self):
        self.u += self.sx
        self.v += self.sy
        self.u, self.v = Limit(self.u, self.v, self.minspeed, self.maxspeed)
        self.x += self.u * dt
        self.y += self.v * dt
        self.sx = self.sy = 0


    def AvoidEdges(self):
        steer_x, steer_y = 0, 0
        buffer = 4
        if self.x <= buffer:
            steer_x += buffer / self.x
        if self.x >= width - buffer:
            steer_x -= buffer / (width - self.x)
        if self.y <= buffer:
            steer_y += buffer / self.y
        if self.y >= height - buffer:
            steer_y -= buffer / (height - self.y)
        
        steer_x, steer_y = Limit(steer_x, steer_y, 0, edge_force)
        self.sx += steer_x
        self.sy += steer_y
    
    
    def AvoidObstacles(self):
    
        see_ahead_length = 5 * Norm(self.u, self.v) / self.maxspeed
        u, v = Limit(self.u, self.v, 1, 1)
        x = self.x + u * see_ahead_length
        y = self.y + v * see_ahead_length
        for i in range(len(Ox)):
            if Distance(x, y, Ox[i], Oy[i]) <= 1 + Or[i]:
                d = Distance(self.x, self.y, Ox[i], Oy[i])
                steer_x = (x - Ox[i])
                steer_y = (y - Oy[i])
                steer_x, steer_y = Limit(steer_x, steer_y, 0, obstacle_force)
                self.sx += steer_x
                self.sy += steer_y

        
    def Alignment(self):
        n, avg_vx, avg_vy = 0, 0, 0
        for neighbour in self.neighbours:
            avg_vx += neighbour.u
            avg_vy += neighbour.v
            n += 1
            
        if n > 0:
            steer_x = avg_vx / n - self.u
            steer_y = avg_vy / n - self.v
            steer_x, steer_y = Limit(steer_x, steer_y, 0, alignment_force)
            self.sx += steer_x
            self.sy += steer_y


    def Cohesion(self):
        n, avg_x, avg_y = 0, 0, 0
        for neighbour in self.neighbours:
            avg_x += neighbour.x
            avg_y += neighbour.y
            n += 1
            
        if n > 0:
            steer_x = avg_x / n - self.x
            steer_y = avg_y / n - self.y
            steer_x, steer_y = Limit(steer_x, steer_y, 0, cohesion_force)
            self.sx += steer_x
            self.sy += steer_y

    
    def Separation(self):
        steer_x, steer_y = 0, 0
        for neighbour in self.neighbours:
            d = Distance(self.x, self.y, neighbour.x, neighbour.y)
            if d < separation_radius ** 2:
                steer_x += (self.x - neighbour.x) / d
                steer_y += (self.y - neighbour.y) / d
                
        steer_x, steer_y = Limit(steer_x, steer_y, 0, separation_force)
        self.sx += steer_x
        self.sy += steer_y
                
    
    def Steer(self):
        self.Alignment()
        self.Cohesion()
        self.Separation()
        self.AvoidObstacles()
        self.AvoidEdges()
        self.sx, self.sy = Limit(self.sx, self.sy, 0, max_steering_force)
        
    
def Update(n):
    
    # Calculate the steering forces for each boid
    for boid in boidList:
        boid.Neighbours(boidList)
        boid.Steer()
        
    # Move and plot each boid
    patches = []
    for boid in boidList:
        boid.Move()  
    
        # Plot agent as an isocelese triangle
        scale = 0.3
        angle = np.arctan2(boid.v, boid.u)
        c, s = np.cos(angle), np.sin(angle)
        verts = np.array([[-1, -1, 1], [2, 0, 1], [-1, 1, 1]])
        T = np.array([[1, 0, 0], [0, 1, 0], [boid.x, boid.y, 1]])
        R = np.array([[c, s, 0],[-s, c, 0], [0, 0, 1]])
        S = np.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
        verts = np.linalg.multi_dot([verts, S, R, T])
        patches.append(plt.Polygon(verts[:,:2]))
        
    collection.set_paths(patches)

    return collection,


# Model parameters
nboids = 100                # number of boids
tmax = 20                  # max time for the simulation
fps = 60                   # frames per second for the animation
dt = 1 / fps               # seconds elapsed during 1 frame of the animation
width, height = 60, 40     # dimensions of the region
detection_radius = 5       # radius for detecting neighbouring agents
separation_radius = 1      # radius for separating agents

# Steering forces
alignment_force = 0.15
cohesion_force = 0.1
separation_force = 0.2
obstacle_force = 1
edge_force = 1
max_steering_force = 0.3

# Define Obstacles (circle centre co-ordinates and radius)
Ox = [20, 40, 30]
Oy = [13, 13, 26]
Or = [4, 4, 4]
# Ox = []

# Generate agent list
np.random.seed(0)
boidList = [boid() for _ in range(nboids)]

# Setup plot
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.axis("off")
patches = [plt.Polygon(np.zeros((3,2))) for _ in range(nboids)]
collection = collections.PatchCollection(patches)
ax.add_collection(collection)
ax.add_patch(plt.Rectangle((0, 0), width, height, fc="none", ec="k", lw=4))
for i in range(len(Ox)):
    ax.add_patch(plt.Circle((Ox[i], Oy[i]), Or[i], fc="gray", ec="k"))

# Create animation 
anim = animation.FuncAnimation(fig, Update, frames=int(tmax * fps), blit=True)
anim.save("boids.mp4", writer=animation.FFMpegWriter(fps=fps))