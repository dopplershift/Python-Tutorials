# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# OO Matplotlib

# <codecell>

# Basic Imports
import numpy as np
import matplotlib.pyplot as plt

# Create data we use later
x = np.random.randn(500)
y = np.random.randn(500)

# <headingcell level=2>

# PyLab

# <codecell>

# Make a scatter plot
plt.scatter(x, y)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.title('Gaussian Data')
plt.show()

# <markdowncell>

# * PyLab interface handles all the magic of figure creation
# * Provides a stateful interface that tracks the current:
#     - Axes (plot area)
#     - Figure (plot window)
# * These are like global variables--it makes it difficult to work with more than one at at time
# * Provides an interface that mimicks that of MatLab

# <headingcell level=2>

# OO Matplotlib

# <codecell>

# Necessary imports for figure creation
from matplotlib.backends.backend_qt4agg import new_figure_manager, show

# Make another scatter plot
fig = new_figure_manager(1).canvas.figure
ax = fig.add_subplot(1, 1, 1) # Could also create manually sized Axes object
ax.scatter(x, y)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title('Gaussian Data')
show()

# <markdowncell>

# * More object-oriented
#     - Makes the code read more like any other Python code
#     - Objects explicitly referenced so no tracking what's "current"
# * End up with backend specific code
# * Often, a hybrid approach is used

# <codecell>

# Make another scatter plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # Could also create manually sized Axes object
ax.scatter(x, y)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title('Gaussian Data')
plt.show()

# <headingcell level=2>

# EXERCISE:

# <markdowncell>

# Make a step plot of the following data without using any calls to pyplot. You'll need to:
# 
# * Create a new figure with new_figure_manager
# * Use the figure to make an Axes
# * Use the Axes to create a step() plot

# <codecell>

t = np.linspace(0, 10, 300)
x = np.sin(2 * pi * 0.1 * t**2)

# Add your code here

# <headingcell level=1>

# Even More Objects

# <markdowncell>

# Every plot method encapsulates several steps:
# 
# * Creating 1 or more Artists which draw on the Axes
# * Setting up transforms, which control where the Artist is drawn
# * Handling missing data
# * Updating Axes attributes

# <markdowncell>

# Let's make a line plot by hand...

# <codecell>

from matplotlib.lines import Line2D
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
line = Line2D(x,y)
ax.add_artist(line)
plt.show()

# <markdowncell>

# Looks good, but limits are off. We should be able to fix by telling the axes to autoscale_view(). Let's also set the color just to see property modification in action.

# <codecell>

ax.autoscale_view()
line.set_color('red')
plt.draw()

# <markdowncell>

# Well that's weird, the view is still off. What happened is that we added the line as a generic Artist. Autoscaling only considers two sources for data limits: lines and patches. Let's try using add_line()...

# <codecell>

line = Line2D(x,y)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.add_line(line)
plt.show()

# <markdowncell>

# So far so good...

# <codecell>

ax.autoscale_view()
line.set_color('green')
line.set_linestyle('dashed')
plt.draw()

# <markdowncell>

# There we go, and for good measure we go ahead and set the linestyle. Axes have the following methods for adding various artist types:
# 
# * add_artist()
# * add_line()
# * add_collection()
# * add_patch()

# <codecell>

from matplotlib.collections import CircleCollection
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sizes = np.empty_like(x)
sizes.fill(20)
coll = CircleCollection(sizes, offsets=(x,y), transOffset=ax.transData, edgecolor='red', facecolor='cyan')
ax.add_collection(coll)
ax.autoscale_view()
plt.draw()

# <markdowncell>

# Let's add a couple of "useful" patches to this.

# <codecell>

from matplotlib.patches import Circle, Rectangle
circ = Circle((0,0), radius=1.0, color='black', alpha=0.7, facecolor='light blue')
ax.add_patch(circ)

rect = Rectangle((-1.5, 1.5), width=0.75, height=0.75, alpha=0.8, facecolor='purple')
ax.add_patch(rect)
plt.draw()

# <headingcell level=2>

# EXERCISE:

# <markdowncell>

# Make a plot without using any plot methods. Any will do, just be sure not to use plotting methods like plot() and scatter() but instead create artists by hand. If you have one you like, go for it, just try to use multiple types of Artist. If nothing springs to mind, try:
# 
# * Line plot
# * 2 Ellipses marking regions of "interest" on the curve
# 
# Some possible Artists:
# 
# * Patches: Rectangle, Circle, Ellipse, Arc, Arrow, Polygon
# * Line2D
# * Collections: LineCollection, CircleCollection, PolyCollection
# 
# You can use any data you like, or just use the following as a starting point:

# <codecell>

om = 0.2
t = np.linspace(0, 10, 300)
x = np.cos(2 * np.pi * om * t) * np.sin(2 * np.pi * (3 * om) * t)

# Add your code here

# <headingcell level=1>

# Wrap Up

# <markdowncell>

# Why would we ever want to know this? Possible reasons:
# 
# * Impress your friends
# *  ...
# * Profit!

# <markdowncell>

# No, really:
# 
# * Good for simple annotations
# * Custom plot elements
# * Forms the basis for creating entire custom plots
# 
# Also it can be useful to understand the guts of what goes into a plot so that we can work with the objects returned from plots, or if we need to mimic some of the Axes' operation ourselves.

# <codecell>

plt.plot(x,y)

# <codecell>

plt.scatter(x,y)

