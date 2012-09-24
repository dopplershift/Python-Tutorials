# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import matplotlib.pyplot as plt

# <headingcell level=1>

# Timers

# <markdowncell>

# Matplotlib backends feature a generic timer object that abstracts away the backend-specific timer objects. Using a timer object allows firing events at a given interval *within* the backend's event loop. The code below uses a timer object to update the time set in the title of the plot.

# <codecell>

from datetime import datetime
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

def updateTime(axes):
    axes.set_title(datetime.now())
    axes.figure.canvas.draw()

timer = fig.canvas.new_timer(interval=100) # This should be enough
timer.add_callback(updateTime, ax)
timer.interval = 100 # Work around bug in QT timer

# Make sure the timer gets stopped when the figure is closed
# since we're holding onto a reference
ax.figure.canvas.mpl_connect('close_event', lambda *a: timer.stop())

timer.start()

# <markdowncell>

# Now we can use a timer to modify the data for a plot object, producing an animation. This is the simplest method, but effective. In this case, we're just changing the points set on a parabola.

# <codecell>

# Make a basic line plot of a parabola
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(0, 20)
y = 0.5 * x * x
line, = ax.plot(x, y)

# Callback to take a line and update the data on it
def updateLine(line, x, y):
    line.set_data(x[:updateLine.i], y[:updateLine.i])
    line.figure.canvas.draw() # Make the figure redraw
    updateLine.i = (updateLine.i + 1) % x.size
# Store the current index as an attribute on the function
updateLine.i = 0

# Make a new timer and add the callback
timer = fig.canvas.new_timer(interval=100)
timer.add_callback(updateLine, line, x, y)
ax.figure.canvas.mpl_connect('close_event', lambda *a: timer.stop())
timer.start()

# <markdowncell>

# This is the same example as before, but uses a class to store state instead of passing parameters to the callback and using a function attribute.

# <codecell>

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(0, 20)
y = 0.5 * x * x
line, = ax.plot(x, y)

# The class only takes a line object as a parameter. All
# of the needed information is obtained from the object itself.
class updatingLine(object):
    def __init__(self, line):
        self._line = line
        self._xdata = line.get_xdata()
        self._ydata = line.get_ydata()
        self.counter = 0
        self.canvas = line.figure.canvas

    def __call__(self):
        self._line.set_data(self._xdata[:self.counter],
            self._ydata[:self.counter])
        self.canvas.draw()
        self.counter = (self.counter + 1) % self._xdata.size

timer = fig.canvas.new_timer(interval=100)
timer.add_callback(updatingLine(line))
ax.figure.canvas.mpl_connect('close_event', lambda *a: timer.stop())
timer.start()

# <headingcell level=2>

# Exercise:

# <markdowncell>

# Make an animation of the following data and plot. You should:
# 
# * Create a callback function that modifies the line objects' data
# * Create a new timer and add the callback to it
# * If running interactively, don't forget to use mpl_connect() to connect to the figure canvas's 'close_event' to make sure the timer is stopped when the figure is closed

# <codecell>

# This creates a plot of a decaying sine/cosine wave
t = np.linspace(0, 10, 500)
x1 = np.exp(-0.5 * t) * np.sin(2 * np.pi * t)
x2 = np.exp(-0.5 * t) * np.cos(2 * np.pi * t)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line1,line2 = plt.plot(t, x1, t, x2)

# Add your code here

# <headingcell level=1>

# Animation Classes

# <markdowncell>

# In addition to animation uses, the timer events can serve other useful purposes since they provide a way to trigger updates within the Figure's event loop. For instance, a timer could be used to check for a file and update the plot with any new data.

# <markdowncell>

# * Animation classes make use of Timer to simplify the process of creating animations
#   - Simplify taking care of repeating, repeat delay, frame interval
#   - Allow for saving animations to movie files (ffmpeg, mencoder)
#   - Can support bltting...in some cases
#   - ArtistAnimation and FuncAnimation

# <markdowncell>

# Here's a basic example that plots a series of Images using ArtistAnimation. ArtistAnimation takes a list of artists to show for each frame. It's simple, but inefficient to create separate artists instead of resetting the data for an artist.

# <codecell>

# Import the two main animation classes
from matplotlib.animation import ArtistAnimation, FuncAnimation

# <codecell>

# Create an empty figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ims = [] # list for storing all of the created artists

# Generate a bunch of images with random data
for i in range(10):
    ims.append([ax.imshow(np.random.randn(20, 20))])

# Create an animation object, passing it the figure and a
# sequence of *collections* of Artists. In this case we are
# giving it a list of lists of images.
# Frames are displayed with a 500 millisecond delay
anim = ArtistAnimation(fig, ims, interval=500)

# <markdowncell>

# Same animation, but this time delaying between restarts of the animation.

# <codecell>

from matplotlib.animation import ArtistAnimation
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ims = []
for i in range(10):
    ims.append([ax.imshow(np.random.randn(20, 20))])

anim = ArtistAnimation(fig, ims, interval=500, repeat_delay=3000)

# <markdowncell>

# We can also make the animation run only once.

# <codecell>

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ims = []
for i in range(10):
    ims.append([ax.imshow(np.random.randn(20, 20))])

anim = ArtistAnimation(fig, ims, interval=500, repeat=False)

# <markdowncell>

# The reason for using a sequence of collections is to allows composing frames of multiple artists. For instance, we can take the random images a step further and move a green dot in a circular pattern around the center. (Pretend this is the output of some feature identification algorithm running on the image data.)

# <codecell>

from matplotlib.patches import Circle
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
artists = []
for i in range(10):
    im = ax.imshow(np.random.randn(20, 20), extent=(-5, 5, -5, 5))
    circle = Circle([2 * cos(i * np.pi / 5.), 2 * sin(i * np.pi / 5.)],
        radius=0.25, color='green', fill=True)
    ax.add_patch(circle)
    artists.append([im, circle])

anim = ArtistAnimation(fig, artists, interval=500, repeat_delay=1500)

# <markdowncell>

# FuncAnimation is more generic, using an arbitrary callback to set the frame for each animation, similar to what was done using just a timer. It is a bit more verbose, but gives greater flexibility in what can be done. Also, it can be more efficient by not creating so many artists but just re-using them with changing data.

# <codecell>

t = np.linspace(0, 10, 500)
x = np.exp(-0.5 * t) * np.sin(2 * np.pi * t)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line, = plt.plot(t, x)

def update_line(frame, line, t, x):
    line.set_data(t[:frame], x[:frame])

anim = FuncAnimation(fig, update_line, fargs=(line, t, x), interval=50)

# <headingcell level=2>

# Exercise:

# <markdowncell>

# Let's redo the timer example with the FuncAnimation class and see how things are simplified. You'll need to:
# 
# * Create a callback function for updating the data on the lines
# * Createa FuncAnimation using this callback and the appropriate list of parameters
# 
# Here is the same starting boilerplate:

# <codecell>

# This creates a plot of a decaying sine/cosine wave
t = np.linspace(0, 10, 500)
x1 = np.exp(-0.5 * t) * np.sin(2 * np.pi * t)
x2 = np.exp(-0.5 * t) * np.cos(2 * np.pi * t)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line1,line2 = plt.plot(t, x1, t, x2)

# Add your code here

# <headingcell level=1>

# Advanced Tricks

# <headingcell level=2>

# Other frame data

# <markdowncell>

# Frame data does not have to be a frame count or even a sequence of frame numbers. Framedata can be:
# 
# * A sequence of anything
# * An iterator
# * A generator
# 
# This gives more flexibility to FuncAnimation in terms of being able to do fully procedural plots instead of being locked into doing just pre-set sequences of frames.

# <codecell>

# Based on this blog post:
# http://glowingpython.blogspot.com/2011/06/animation-with-matplotlib-bringin.html
from matplotlib.lines import Line2D

# Generator for producing new data
def make_data():
    A = np.array([ [.5, 0], [0, .5] ])
    b1 = np.array([0, 0])
    b2 = np.array([.5, 0])
    b3 = np.array([.25, np.sqrt(3)/4])
    b = [b1, b2, b3]
    x = np.array([0, 0])
    while True:
        x = dot(A, x) + b[np.random.randint(0, 3)]
        yield x

# Function for generating new random data procedurally
# We store the data in a list since it's good for appending.
# However, you do end up copying a lot of data to arrays eventually.
x = []
y = []
def update_line(newData, l, x, y):
    newX, newY = newData
    x.append(newX)
    y.append(newY)
    l.set_data(x, y)
    return l,

# Create a plot with some initial random data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line = Line2D([0], [0], markersize=6, color='m', marker='.', linestyle='none')
ax.add_line(line)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Used to clear axes for blitting
def init_blit():
    line.set_data([], [])
    return line,

# Pass in our generator as the frames parameter
anim = FuncAnimation(fig, update_line, frames=make_data, fargs=(line, x, y), interval=10,
    blit=True, init_func=init_blit)

# <headingcell level=2>

# Saving to file

# <markdowncell>

# Creating animations for use when running analytical scripts is nice, but it's really nice to be able to save them for inclusion on the web or in presentations. Matplotlib's animation library features support for creating movie files using one of two "backends":
# 
# * ffmpeg
# * mencoder
# 
# In matplotlib git master, the movie writing support has undergone a substantial internal refactor. As a result, it is much easier to pass custom encoding options to control the codec and quality used for the resulting movie. Also, unix pipes are employed by default when using the ffmpeg/mencoder utility, drastically speeding up the write process.
# 
# However, we will demonstrate saving files with the Matplotlib 1.1 code, whose API for the most part has only been extended.

# <codecell>

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ims = []
for i in range(50):
    ims.append([ax.imshow(np.random.randn(20, 20))])

anim = ArtistAnimation(fig, ims, interval=500, repeat=False)
anim.save('images.mp4', fps=15)

# <headingcell level=2>

# Blitting

# <markdowncell>

# Blitting is a technique for increasing animation performance by only drawing things that have changed. However, this requires:
# 
# * An init_func for creating a clean slate (for erasing between frames)
# * Knowledge of what artists change in a frame so that only those are drawn
# 
# As a result, blitting is not enabled by default.

# <codecell>

# This creates a plot of a decaying sine/cosine wave
t = np.linspace(0, 10, 500)
x1 = np.exp(-0.5 * t) * np.sin(2 * np.pi * t)
x2 = np.exp(-0.5 * t) * np.cos(2 * np.pi * t)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line1,line2 = plt.plot(t, x1, t, x2)

def update_lines(frame, line1, line2, t, x1, x2):
    line1.set_data(t[:frame], x1[:frame])
    line2.set_data(t[:frame], x2[:frame])
    return line1, line2 # Added for blitting

# This is created for blitting
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

anim = FuncAnimation(fig, update_lines, frames=t.size, fargs=(line1, line2, t, x1, x2), interval=10,
    init_func=init, blit=True)

# <headingcell level=2>

# John Hunter's Double Pendulum Demo

# <codecell>

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

from numpy import sin, cos, pi, array
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

G =  9.8 # acceleration due to gravity, in m/s^2
L1 = 1.0 # length of pendulum 1 in m
L2 = 1.0 # length of pendulum 2 in m
M1 = 1.0 # mass of pendulum 1 in kg
M2 = 1.0 # mass of pendulum 2 in kg


def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    del_ = state[2]-state[0]
    den1 = (M1+M2)*L1 - M2*L1*cos(del_)*cos(del_)
    dydx[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_)
               + M2*G*sin(state[2])*cos(del_) + M2*L2*state[3]*state[3]*sin(del_)
               - (M1+M2)*G*sin(state[0]))/den1

    dydx[2] = state[3]

    den2 = (L2/L1)*den1
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_)
               + (M1+M2)*G*sin(state[0])*cos(del_)
               - (M1+M2)*L1*state[1]*state[1]*sin(del_)
               - (M1+M2)*G*sin(state[2]))/den2

    return dydx

# create a time array from 0..100 sampled at 0.1 second steps
dt = 0.05
t = np.arange(0.0, 20, dt)

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
th1 = 120.0
w1 = 0.0
th2 = -10.0
w2 = 0.0

rad = pi/180

# initial state
state = np.array([th1, w1, th2, w2])*pi/180.

# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)

x1 = L1*sin(y[:,0])
y1 = -L1*cos(y[:,0])

x2 = L2*sin(y[:,2]) + x1
y2 = -L2*cos(y[:,2]) + y1

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template%(i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
    interval=25, blit=True, init_func=init)

# <headingcell level=2>

# Exercise:

# <markdowncell>

# Let's animate a complex, multi-panel plot. Since the Animation objects work at the Figure level, this does not create too much more complexity, just more plot objects. Given the x, y, z dataset below, create and animate:
# 
# * panel with x versus z
# * panel with y versus z
# * panel with x versus y
# 
# In these plots, be sure to make the current point stand out from the rest of the data.
# 
# This animation can be done as a straightforward extension of the previous examples. However, due to the amount of state that has to be managed (multiple lines, etc.) you may want to try using a class to store the state and have an instance's method as the callback.

# <codecell>

t = np.linspace(0, 80, 400)
x = np.cos(2 * np.pi * t / 10.)
y = np.sin(2 * np.pi * t / 10.)
z = 10 * t

# Add your code here

