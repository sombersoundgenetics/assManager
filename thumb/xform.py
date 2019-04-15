import numpy as np

def rot(t, axis):

    #solve terms
    cost = np.cos(t)
    sint = np.sin(t)

    #solve rotations along x
    if axis == 0 or axis is "x":
        m = np.matrix([
            [1,         0,      0,      0],
            [0,         cost,   -sint,  0],
            [0,         sint,   cost,   0],
            [0,         0,      0,      1]])
    #solve rotations around y
    elif axis == 1 or axis is "y":
        m = np.matrix([
            [cost,      0,      sint,   0],
            [0,         1,      0,      0],
            [-sint,     0,      cost,   0],
            [0,         0,      0,      1]])
    #solve rotations around z
    elif axis == 2 or axis is "z":
        m = np.matrix([
            [cost,      -sint,  0,      0],
            [sint,      cost,   0,      0],
            [0,         0,      1,      0],
            [0,         0,      0,      1]])
    #return identity matrix as default
    else:
        m = np.matrix([
            [1,         0,      0,      0],
            [0,         1,      0,      0],
            [0,         0,      1,      0],
            [0,         0,      0,      1]])


    #return the matrix
    return m


def trans(t, axis) :
    # solve rotations along x
    if axis == 0 or axis is "x":
        m = np.matrix([
            [1,         0,      0,      0],
            [0,         1,      0,      0],
            [0,         0,      1,      0],
            [t,         0,      0,      1]])
    # solve rotations around y
    elif axis == 1 or axis is "y":
        m = np.matrix([
            [1,         0,      0,      0],
            [0,         1,      0,      0],
            [0,         0,      1,      0],
            [0,         t,      0,      1]])
    # solve rotations around z
    elif axis == 2 or axis is "z":
        m = np.matrix([
            [1,         0,      0,      0],
            [0,         1,      0,      0],
            [0,         0,      1,      0],
            [0,         0,      t,      1]])
    # return identity matrix as default
    else:
        m = np.matrix([
            [1,         0,      0,      0],
            [0,         1,      0,      0],
            [0,         0,      1,      0],
            [0,         0,      0,      1]])

    return m

def v2m(vec):
    return np.matrix([
        [1,      0,      0,      0],
        [0,      1,      0,      0],
        [0,      0,      1,      0],
        [vec[0], vec[1], vec[2], 1]])

def cameraMatrix(bounds, pan, tilt, fov, dist):
    #convert bounds to numpy array
    bounds = np.array([[bounds.min.x, bounds.min.y, bounds.min.z], [bounds.max.x, bounds.max.y, bounds.max.z]])

    # define the pan/tilt angles and solve the transform matrices
    mRx = rot(np.radians(tilt), 0)
    mRy = rot(np.radians(pan), 1)

    # compose the rotational transform
    mR = np.matmul(mRx, mRy)

    # solve the z position from the diagonal distance of bounds
    h = np.abs(np.linalg.norm(bounds[0] - bounds[1]))
    z = (h / 2) / np.tan(np.radians(fov / 2))

    #solver the center of the bounds
    c = np.multiply(np.add(bounds[0],bounds[1]),0.5)
    #translation matrix to center
    mC = v2m(c)

    #define the translation matrix along z
    mT = trans(z,"z")

    # solve the cameras transform matrix
    m = np.matmul(np.matmul(mT, mR),mC)

    # return the matrix
    return m

