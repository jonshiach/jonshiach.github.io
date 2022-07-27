#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:11:47 2022

@author: jon
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, collections

class boid:
    
    def __init__(self):
        self.x = width * np.random.rand()   # x co-ordinate
        self.y = height * np.random.rand()  # y co-ordinate
        self.vx = np.random.uniform(-1, 1)  # velocity in the x direction
        self.vy = np.random.uniform(-1, 1)  # velocity in the y direction
        self.sx = 0                         # steering force in the x direction
        self.sy = 0                         # steering force in the y direction
        self.minspeed = 5                   # minimum speed of the agent
        self.maxspeed = 10                  # maximum speed of the agent
        self.neighbours = []                # list of neighbouring agents
        self.vx, self.vy = Limit(self.vx, self.vy, self.minspeed, self.maxspeed)
       

    def Neighbours(self, boidList):
        self.neighbours = []
        for neighbour in boidList: 
            if id(self) == id(neighbour):
                continue
            dx = neighbour.x - self.x
            dy = neighbour.y - self.y
            if abs(dx) < detection_radius and abs(dy) < detection_radius:
                d = dx ** 2 + dy ** 2
                if d < detection_radius ** 2:
                    self.neighbours.append(neighbour)
                    
                    
    def Move(self):
        self.vx += self.sx
        self.vy += self.sy
        self.vx, self.vy = Limit(self.vx, self.vy, self.minspeed, self.maxspeed)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.sx = self.sy = 0


    def AvoidEdges(self):
        buffer = 2
        if self.x < buffer:
            self.sx += 1 / self.x ** 2
        if self.x > width - buffer:
            self.sx -= 1 / (width - self.x) ** 2
        if self.y < buffer:
            self.sy += 1 / self.y ** 2
        if self.y > height - buffer:
            self.sy -= 1 / (height - self.y) ** 2
        

    def AvoidObstacles(self):
        vx, vy = Limit(self.vx, self.vy, detection_radius, detection_radius)
        aheadx = self.x + vx
        aheady = self.y + vy
        dmin = 1e6
        for i in range(len(obs_x)):
            d = (aheadx - obs_x[i]) ** 2 + (aheady - obs_y[i]) ** 2
            if d < obs_r[i] ** 2 and d < dmin:
                cx = obs_x[i]
                cy = obs_y[i]
                r = obs_r[i]
                dmin = d
                
        if dmin < 1e6:
            steer_x = aheadx - cx
            steer_y = aheady - cy
            d = steer_x ** 2 + steer_y ** 2
            self.sx, self.sy = Limit(steer_x, steer_y, 1, 1)
            
        
        
    def Alignment(self):
        n, steer_x, steer_y = 0, 0, 0
        for neighbour in self.neighbours:
            steer_x += neighbour.vx
            steer_y += neighbour.vy
            n += 1
            
        if n > 0:
            steer_x = steer_x / n - self.vx
            steer_y = steer_y / n - self.vy
            self.sx, self.sy = Limit(steer_x, steer_y, 0, alignment_force)


    def Cohesion(self):
        n, steer_x, steer_y = 0, 0, 0
        for neighbour in self.neighbours:
            steer_x += neighbour.x
            steer_y += neighbour.y
            n += 1
            
        if n > 0:
            steer_x = steer_x / n - self.x
            steer_y = steer_y / n - self.y
            self.sx, self.sy = Limit(steer_x, steer_y, 0, cohesion_force)

    
    def Separation(self):
        steer_x, steer_y = 0, 0
        for neighbour in self.neighbours:
            d = (self.x - neighbour.x) ** 2 + (self.y - neighbour.y) ** 2
            if d < separation_radius ** 2:
                steer_x += (self.x - neighbour.x) / d
                steer_y += (self.y - neighbour.y) / d
                
        self.sx, self.sy = Limit(steer_x, steer_y, 0, separation_force)
                
    
    def Steer(self):
        self.Alignment()
        self.Cohesion()
        self.Separation()
        self.sx, self.sy = Limit(self.sx, self.sy, 0, max_steering_force)
        self.AvoidEdges()
        self.AvoidObstacles()


def ScaleVector(vx, vy, scale):
    norm = np.sqrt(vx ** 2 + vy ** 2)
    if norm > 0:
        vx = vx / norm * scale
        vy = vy / norm * scale
    
    return vx, vy


def Limit(vx, vy, lower, upper):
    norm = np.sqrt(vx ** 2 + vy ** 2)
    if norm < lower:
        vx = vx / norm * lower
        vy = vy / norm * lower
    elif norm > upper:
        vx = vx / norm * upper
        vy = vy / norm * upper
        
    return vx, vy

    
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
        angle = np.arctan2(boid.vy, boid.vx)
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
nboids = 50                # number of boids
tmax = 20                  # max time for the simulation
fps = 60                   # frames per second for the animation
dt = 1 / fps               # time elapsed during 1 frame
width, height = 60, 40     # dimensions of the region
detection_radius = 5       # radius for detecting neighbouring agents
separation_radius = 2      # radius for separating agents

# Steering forces
alignment_force = 0.1
cohesion_force = 0.05
separation_force = 0.1
max_steering_force = 0.2  

# Define Obstacles (circle centre co-ordinates and radius)
obs_x = [20, 40]
obs_y = [20, 20]
obs_r = [5, 5]

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
for i in range(len(obs_x)):
    ax.add_patch(plt.Circle((obs_x[i], obs_y[i]), obs_r[i], ec="k", fc="none"))

# Create and save animation 
import time
start = time.time()
anim = animation.FuncAnimation(fig, Update, frames=tmax * fps, blit=True)
anim.save("boids.mp4", writer=animation.FFMpegWriter(fps=fps))

print(time.time() - start)