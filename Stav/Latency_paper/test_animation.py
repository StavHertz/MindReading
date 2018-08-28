"""
============
3D animation
============

A simple example of an animated plot... In 3D!
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


def Gen_RandLine(length, dims=2):
    """
    Create a line using a random walk algorithm

    length is the number of points for the line.
    dims is the number of dimensions the line has.
    """
    lineData = np.empty((dims, length))
    lineData[:, 0] = np.random.rand(dims)
    for index in range(1, length):
        # scaling the random numbers by 0.1 so
        # movement is small compared to position.
        # subtraction by 0.5 is to change the range to [-0.5, 0.5]
        # to allow a line to move backwards.
        step = ((np.random.rand(dims) - 0.5) * 0.1)
        lineData[:, index] = lineData[:, index - 1] + step

    return lineData


def get_rand_dot(length, dims=2):
    dot_data =np.empty((dims, length))
    dot_data[:, 0] = np.random.rand(dims)
    for ind in range(1, length):
        step = ((np.random.rand(dims) - 0.5) * 0.1)
        dot_data[:, ind] = dot_data[:, ind - 1] + step
    return dot_data

def update_dots(num, data_dots, dots):
    for dot, data in zip(dots, data_dots):
        dot.set_sizes(data[:, 0]*num*10)
    print("done")
    return dots

def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
# data = [Gen_RandLine(25, 3) for index in range(50)]
data = [get_rand_dot(25, 3) for index in range(50)]

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
dots = [ax.scatter(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1]) for dat in data]
# lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]
print(dots[0])
# Setting the axes properties
ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_dots, 25, fargs=(data, dots),
                                   interval=50, blit=False)

plt.show()