'''
animations.py by Dr Jon Shiach, January 2022

This python script contains functions used to produce animations for the Jupyter 
notebook 'Chaos with Python'
'''

# Import libraries
from numpy import *
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML, YouTubeVideo
from scipy.integrate import solve_ivp
from ipywidgets import IntProgress

def plotpendulum(t, x, y):
    '''
    This function plots a single pendulum solution and outputs an animation object.
    '''
    # Create plot figure
    fig, ax = plt.subplots(figsize=(12,5))
    ax.set_xlim([amin(x) - 0.2, amax(x) + 0.2])
    ax.set_ylim([amin(y) - 0.2, amax(y) + 0.2])
    ax.set_aspect('equal')
    plt.axis('off')

    # Create plot objects
    fps = int(1 / (t[1] - t[0]))
    obj, ns, s = [], 20, 2 * fps // 20
    ax.plot([0], [0], 'k.', ms=20, zorder=10)[0]
    obj.append(ax.plot([], [], '-', c = 'b', lw=2)[0])
    obj.append(ax.plot([], [], marker='.', ms=20, c='b', zorder=5)[0])
    for j in range(ns):
        obj.append(ax.plot([], [], '-', c='b', alpha=(j/ns)**2, solid_capstyle='butt')[0])

    # Create progress bar
    progress_bar = IntProgress(min=0, max=x.shape[1], description="Animating")
    display(progress_bar)

    # Plot current frame
    def animate(n):
        obj[0].set_data([x[:2,n]], [y[:2,n]])
        obj[1].set_data([x[1,n]], [y[1,n]])
        for i in range(ns):
            imin = n - (ns - i) * s
            imax = imin + s + 1
            if imin < 0 and imax > 0:
                imin = 0
                obj[i+2].set_data([x[1,imin:imax]], [y[1,imin:imax]])
            elif imin >= 0:
                obj[i+2].set_data([x[1,imin:imax]], [y[1,imin:imax]]) 
        progress_bar.value += 1
        return obj
          
    # Create animation
    anim = animation.FuncAnimation(fig,  animate, frames=len(t), interval=1000 / fps, blit=True)
    plt.close()
    
    return anim


def plotdoublependulum(t, x, y):
    '''
    This function plots a double pendulum solution and outputs an animation object.
    '''
    # Create plot figure
    fig, ax = plt.subplots(figsize=(12,5))
    ax.set_xlim([amin(x) - 0.2, amax(x) + 0.2])
    ax.set_ylim([amin(y) - 0.2, amax(y) + 0.2])
    ax.set_aspect('equal')
    plt.axis('off')

    # Create plot objects
    N, fps = x.shape[0] // 3, int(1 / (t[1] - t[0]))
    obj, ns, s = [], 20, 2 * fps // 20
    ax.plot([0], [0], 'k.', ms=20, zorder=10)[0] # pivot
    for i in range(N):
        obj.append(ax.plot([], [], 'b-', lw=2)[0]) # rod 1
        obj.append(ax.plot([], [], 'r-', lw=2)[0]) # rod 2
        obj.append(ax.plot([], [], marker='.', ms=20, c='b', zorder=5)[0]) # weight 1
        obj.append(ax.plot([], [], marker='.', ms=20, c='r', zorder=5)[0]) # weight 2
        for j in range(ns):
            obj.append(ax.plot([], [], 'r-', alpha=(j/ns)**2, solid_capstyle='butt')[0])

    # Create progress bar
    progress_bar = IntProgress(min=0, max=x.shape[1], description="Animating")
    display(progress_bar)

    # Plot current frame
    def animate(n):
        k = 0
        for i in range(N):
            obj[k].set_data([x[3*i:3*i+2,n]], [y[3*i:3*i+2,n]])
            obj[k+1].set_data([x[3*i+1:3*i+3,n]], [y[3*i+1:3*i+3,n]])
            obj[k+2].set_data([x[3*i+1,n]], [y[3*i+1,n]])
            obj[k+3].set_data([x[3*i+2,n]], [y[3*i+2,n]])
            k += 4
            for j in range(ns):
                jmin = n - (ns - j) * s
                jmax = jmin + s + 1
                if jmin < 0 and jmax > 0:
                    jmin = 0
                    obj[k].set_data([x[3*i+2,jmin:jmax]], [y[3*i+2,jmin:jmax]])
                elif jmin >= 0:
                    obj[k].set_data([x[3*i+2,jmin:jmax]], [y[3*i+2,jmin:jmax]])
                k += 1  
        
        # Progress bar
        progress_bar.value += 1

        return obj
          
    # Create animation
    anim = animation.FuncAnimation(fig,  animate, frames=len(t), interval=1000 / fps, blit=True)
    plt.close()
    
    return anim


def plotNbody(sol):
    '''
    This function plots the motion of an N body problem
    '''
    # Extract t and x and y co-ordinates
    N = sol.y.shape[0] // 4
    t = sol.t
    x, y = sol.y[:2 * N:2], sol.y[1:2 * N + 1:2]
    fps = int(1 / (t[1] - t[0]))
    
    # Create plot figure
    fig, ax = plt.subplots(figsize=(12,5))
    ax.set_xlim([amin(x) - 0.2, amax(x) + 0.2])
    ax.set_ylim([amin(y) - 0.2, amax(y) + 0.2])
    ax.set_aspect('equal')
    plt.axis('off')

    # Create plot objects
    col, obj, ns, s = ['b', 'r', 'g', 'k', 'c', 'm', 'y'], [], 20, fps // 20
    for i in range(N):
        obj.append(ax.plot([], [], marker='.', ms=20, c=col[i], zorder=10)[0])
        for j in range(ns):
            obj.append(ax.plot([], [], '-', c=col[i], alpha=(j/ns)**2, solid_capstyle='butt')[0])
    
    # Create progress bar
    progress_bar = IntProgress(min=0, max=x.shape[1], description="Animating")
    display(progress_bar)

    # Plot current frame
    def animate(n):
        k = 0
        for i in range(N):
            obj[k].set_data([x[i,n]], [y[i,n]])
            k += 1
            for j in range(ns):
                jmin = n - (ns - j) * s
                jmax = jmin + s + 1
                if jmin < 0 and jmax > 0:
                    jmin = 0
                    obj[k].set_data([x[i,jmin:jmax]], [y[i,jmin:jmax]])
                elif jmin >= 0:
                    obj[k].set_data([x[i,jmin:jmax]], [y[i,jmin:jmax]])
                k += 1 

        # Progress bar
        progress_bar.value += 1

        return obj
        
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=len(t), interval=2000 / fps , blit=True)
    plt.close()
    
    return anim