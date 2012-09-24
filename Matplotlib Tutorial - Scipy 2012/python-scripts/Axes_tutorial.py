# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Set up some data
#%pylab inline
import numpy as np
import matplotlib.pyplot as plt
x = np.random.randn(100)
y = np.random.randn(9, 100)

# <headingcell level=1>

# Basic Axes Layouts

# <markdowncell>

# The original way to get layouts of axes is the MatLab-style subplot() command.

# <codecell>

fig = plt.figure()
for i in range(9):
    ax = fig.add_subplot(3, 3, i + 1)
    ax.plot(1000 * x, 1000 * y[i])

# <markdowncell>

# Of course, to make sure of sharing axes is an utter pain this way:

# <codecell>

fig = plt.figure()
shareAx = None
for i in range(9):
    ax = fig.add_subplot(3, 3, i + 1, sharex=shareAx, sharey=shareAx)
    ax.plot(1000 * x, 1000 * y[i])
    if shareAx is None:
        shareAx = ax

# <markdowncell>

# With subplot(), you need to create each axes object individually. subplots() eliminates this and allows you to create all the axes in one go. For many applications, this elminates code duplication and makes scripts easier to maintain.

# <codecell>

fig, axes = plt.subplots(3, 3, sharex=True, sharey=True)
for i,ax in enumerate(axes.flat):
    ax.plot(1000 * x, 1000 * y[i])

# <codecell>

axes

# <markdowncell>

# As you can see, the problem of overlapping labels is handled by removing the redundant labels. But what about the case where the labels are not redundant?

# <codecell>

fig, axes = plt.subplots(3, 3)
for i,ax in enumerate(axes.flat):
    ax.plot(x**(i+1), y[i]**(i+1))
fig.tight_layout()
plt.draw()

# <markdowncell>

# tight_layout() adjusts the sizes of all the Axes to ensure that there is sufficient room for the text labels between the Axes objects. This helps resolve the problem but does not help when tick labels overlap each other. Axes.locator_params is a helper that makes it easier to adjust parameters on the tick Locators. In this case, we tell the MaxNLocator (which is used by default) to only have at most 4 increments between ticks.

# <codecell>

fig, axes = plt.subplots(3, 3)
for i,ax in enumerate(axes.flat):
    ax.plot(x**(i+1), y[i]**(i+1))
    ax.locator_params(axis='both', nbins=4)
fig.tight_layout()
plt.draw()

# <markdowncell>

# Better, but there's still quite a bit of overlap on some of them. We can improve it by adjusting the formatting of the labels to use scientific notation. ticklabel_format() is a helper that allows us to control this easily. In this case, we change the scientific notation limit of the default ScalarFormatter.

# <codecell>

fig, axes = plt.subplots(3, 3)
for i,ax in enumerate(axes.flat):
    ax.plot(x**(i+1), y[i]**(i+1))
    ax.locator_params(axis='both', nbins=4)
    ax.ticklabel_format(scilimits=(-1, 1))
fig.tight_layout()
plt.draw()

# <headingcell level=2>

# Exercise:

# <markdowncell>

# Take the following data and make a set of scatter plots with 2 rows and 4 columns. Each row should plot either x[0] or x[1] and each column should plot the Y data appropriate to that panel (i.e. the 2nd row and 3rd column should plot y[1][2]). You should experiment with sharing any appropriate axes and seeing what can be done to produce clean tick (non-overlapping) ticks.

# <codecell>

x = np.array([20 * np.random.rand(100) - 10, 10 * np.random.randn(100)])
y = np.array([x, x**2, x**3, x**4])
y = y.swapaxes(0, 1) # To make Y have shape (2, 4, 100)

# Your code here

# <headingcell level=1>

# Advanced Layouts

# <headingcell level=2>

# subplot2grid()

# <markdowncell>

# Matplotlib also has support for more advanced layouts for when uniformly sized axes are insufficient. One method for this is subplot2grid, which uses a subplot-like syntax to allow for axes that span multiple locations.

# <codecell>

# Time to change up the data
om = 0.2
t = np.linspace(0, 5)
x1 = np.sin(2 * np.pi * om * t)
x2 = np.sin(2 * np.pi * (2 * om) * t)
x3 = np.sin(2 * np.pi * (3 * om) * t)

# <codecell>

fig = plt.figure()
ax = plt.subplot2grid((2, 3), loc=(0, 0), colspan=2)
ax.plot(t, x1)

ax = plt.subplot2grid((2, 3), loc=(0, 2))
ax.plot(t, x2)

ax = plt.subplot2grid((2, 3), loc=(1, 0), colspan=3)
ax.plot(t, x3)

fig.tight_layout()
plt.draw()

# <headingcell level=2>

# AxesDivider and ImageGrid

# <rawcell>

# AxesGrid is a toolkit for Matplotlib that adds a layout engine for managing the locations of Axes. It is more complex to use, but offers complete control of how the Axes are laid out. This includes a variety of ways to specify sizes (physical and relative units) and sizes of spaces between them.

# <codecell>

from mpl_toolkits.axes_grid1 import make_axes_locatable
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(t, x1)

# Set up the divider on the axes
divider = make_axes_locatable(ax)

# Add one axis to the right
ax2 = divider.append_axes('right', size='33%', pad=0.5)
ax2.plot(t, x2)

# And another..
ax3 = divider.append_axes('right', size='33%', pad=0.5)
ax3.plot(t, x3)

# <markdowncell>

# make_axes_locatable() gives one way to handle this, by giving the append_axes() method. Another way is by creating a Divider object and giving it the layout up front.

# <codecell>

from mpl_toolkits.axes_grid1 import Size, Divider
fig = plt.figure()
ax = [fig.add_axes([0.1,0.1,0.8,0.8], label='%d'%i) for i in range(3)] # Create 3 Axes to be sized later
horiz = [Size.Scaled(2), Size.Fixed(0.5), Size.Scaled(3), Size.Fixed(0.01)]
vert = [Size.Scaled(1), Size.Fixed(0.5), Size.Scaled(1)]

div = Divider(fig, (0.1, 0.1, 0.8, 0.8), horiz, vert, aspect=False)

ax[0].set_axes_locator(div.new_locator(nx=0, ny=0))
ax[1].set_axes_locator(div.new_locator(nx=2, ny=0))
ax[2].set_axes_locator(div.new_locator(nx=0, nx1=2, ny=2))

ax[0].plot(t, x1)
ax[1].plot(t, x2)
ax[2].plot(t, x3)

# <rawcell>

# One obvious application of this is for doing grid of plots with colorbars. For this use case we can go one step further and make use of the ImageGrid class.

# <codecell>

from mpl_toolkits.axes_grid1 import ImageGrid
x = y = np.linspace(-3, 3, 300)
data = np.sin(2 * x[:, None]) * np.sin(2 * y)

fig = plt.figure()
grid = ImageGrid(fig, (1, 1, 1), nrows_ncols=(2, 2), axes_pad=0.4,
                 add_all=True, label_mode='L', cbar_mode='each',
                 cbar_location='right', cbar_pad=0.05)

cmaps = ['spring', 'summer', 'autumn', 'winter']
for i in range(4):
    im = grid[i].imshow(data, extent=(-3, 3, -3, 3), cmap=cmaps[i])
    grid.cbar_axes[i].colorbar(im)

# <codecell>

fig = plt.figure()
grid = ImageGrid(fig, (1, 1, 1), nrows_ncols=(2, 2), axes_pad=0.2,
                 add_all=True, label_mode='L', cbar_mode='single',
                 cbar_location='right', cbar_pad=0.1)

for i in range(4):
    im = grid[i].imshow(data + 0.25 * np.random.randn(*data.shape),
        extent=(-3, 3, -3, 3), cmap='summer')
grid.cbar_axes[0].colorbar(im)
plt.draw()

# <markdowncell>

# The axes_grid toolkit provides one other useful tool for automatic layout, but this one isn't for Axes: the AnchoredArtist. Essentially, this provides a set of Artists that can be anchored to a specific part of a figure. This is extremely useful for things like subpanel labels.

# <codecell>

from mpl_toolkits.axes_grid1.anchored_artists import AnchoredText

# <codecell>

# This is adapted from Matplotlib's example on anchored artists
import mpl_toolkits.axes_grid1.anchored_artists as AA
from matplotlib.patches import Circle

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

at = AA.AnchoredText("Figure 1a",
                     loc=2, prop=dict(size=8), frameon=True,
                     )
at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
ax.add_artist(at)

at2 = AnchoredText("Figure 1(b)",
                   loc=3, prop=dict(size=8), frameon=True,
                   bbox_to_anchor=(0., 1.),
                   bbox_transform=ax.transAxes
                   )
at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
ax.add_artist(at2)

ada = AA.AnchoredDrawingArea(20, 20, 0, 0,
                          loc=1, pad=0., frameon=False)
p = Circle((10, 10), 10)
ada.da.add_artist(p)
ax.add_artist(ada)

# draw an ellipse of width=0.1, height=0.15 in the data coordinate
ae = AA.AnchoredEllipse(ax.transData, width=0.1, height=0.15, angle=0.,
                     loc=3, pad=0.5, borderpad=0.4, frameon=True)

ax.add_artist(ae)

# draw a horizontal bar with length of 0.1 in Data coordinate
# (ax.transData) with a label underneath.
asb = AA.AnchoredSizeBar(ax.transData,
                      0.1,
                      r"1$^{\prime}$",
                      loc=8,
                      pad=0.1, borderpad=0.5, sep=5,
                      frameon=False)
ax.add_artist(asb)

# <headingcell level=2>

# Exercise

# <markdowncell>

# Let's make a combined scatter and histogram plot. Take the data below and make a plot with three elements. The main plot should be a square axes with a scatter plot of the x and y data. To the right of this main axes should be vertical histogram of the y data, so that the y values are plotted along this axes' Y-axis. Above the main plot should be a horizontal histogram of the x data. (**Bonus points:** Put text boxes anchored to the panels' corners labelling them.)

# <codecell>

x,y = np.random.randn(2, 300)

# Start adding code here

