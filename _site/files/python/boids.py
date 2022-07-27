#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:54:26 2022

@author: Jon Shiach
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
        self.minspeed = 5                   # minimum speed of the agent
        self.maxspeed = 10                  # maximum speed of the agent
        self.neighbours = []                # list of neighbouring agents
       

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
                    
                    
    def MoveBoid(self):
        self.vx += self.sx
        self.vy += self.sy
        speed = np.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed < self.minspeed:
            self.vx *= self.minspeed / speed
            self.vy *= self.minspeed / speed
        if speed > self.maxspeed:
            self.vx *= self.maxspeed / speed
            self.vy *= self.maxspeed / speed
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.sx = self.sy = 0


    def AvoidEdges(self):
        buffer = 5
        if self.x < buffer:
            self.sx += 1 / self.x ** 2
        if self.x > width - buffer:
            self.sx -= 1 / (width - self.x) ** 2
        if self.y < buffer:
            self.sy += 1 / self.y ** 2
        if self.y > height - buffer:
            self.sy -= 1 / (height - self.y) ** 2
        

    def Alignment(self):
        n = u_avg = v_avg = 0
        for neighbour in self.neighbours:
            u_avg += neighbour.vx
            v_avg += neighbour.vy
            n += 1
        if n > 0:
            self.sx += u_avg / n - self.vx
            self.sy += v_avg / n - self.vy


    def Cohesion(self):
        n = x_avg = y_avg = 0
        for neighbour in self.neighbours:
            x_avg += neighbour.x
            y_avg += neighbour.y
            n += 1
        if n > 0:
            self.sx += x_avg / n - self.x
            self.sy += y_avg / n - self.y

    
    def Separation(self):
        for neighbour in self.neighbours:
            d = (self.x - neighbour.x) ** 2 + (self.y - neighbour.y) ** 2
            if d < separation_radius ** 2:
                self.sx += (self.x - neighbour.x) / d
                self.sy += (self.y - neighbour.y) / d


def Update(n):
    
    # Calculate the steering forces for each boid
    for boid in boidList:
        boid.Neighbours(boidList)
        boid.AvoidEdges()
        boid.Alignment()
        boid.Cohesion()
        boid.Separation()
        
    # Move and plot each boid
    patches = []
    for boid in boidList:
        boid.MoveBoid()  
    
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
nboids = 50               # number of boids
tmax = 20                  # max time for the simulation
fps = 60                   # frames per second for the animation
dt = 1 / fps               # time elapsed during 1 frame
width, height = 60, 40     # dimensions of the region
detection_radius = 5       # radius for detecting neighbouring agents
separation_radius = 2      # radius for separating agents
alignment_factor = 0.1     # alignment steering factor
cohesion_factor = 0.05     # cohesion steering factor
separation_factor = 0.1    # separation steering factor

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

# Create and save animation 
import time
start = time.time()
anim = animation.FuncAnimation(fig, Update, frames=tmax * fps, blit=True)
anim.save("boids.mp4", writer=animation.FFMpegWriter(fps=fps))

print(time.time() - start)