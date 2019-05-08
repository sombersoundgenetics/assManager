import numpy as np


class xform:
    def __init__(self):
        self.identity = np.matrix([
                [1,         0,      0,      0],
                [0,         1,      0,      0],
                [0,         0,      1,      0],
                [0,         0,      0,      1]])

    class rot:
        def __init__(self):
            self.Test = True

        def x(self, theta):
            cost = np.cos(theta)
            sint = np.sin(theta)

            return np.matrix([
                [1,         0,      0,      0],
                [0,         cost,   -sint,  0],
                [0,         sint,   cost,   0],
                [0,         0,      0,      1]])

        def y(self,theta):
            cost = np.cos(theta)
            sint = np.sin(theta)

            return np.matrix([
                [cost,      0,      sint,   0],
                [0,         1,      0,      0],
                [-sint,     0,      cost,   0],
                [0,         0,      0,      1]])

        def z(self,theta):
            cost = np.cos(theta)
            sint = np.sin(theta)

            return np.matrix([
                [cost,      -sint,  0,      0],
                [sint,      cost,   0,      0],
                [0,         0,      1,      0],
                [0,         0,      0,      1]])

    class trans:
        def __init__(self):
            self.test = True

        def x(self, t):
            return np.matrix([
                [1,         0,      0,      0],
                [0,         1,      0,      0],
                [0,         0,      1,      0],
                [t,         0,      0,      1]])

        def y(self, t):
            return np.matrix([
                [1,         0,      0,      0],
                [0,         1,      0,      0],
                [0,         0,      1,      0],
                [0,         t,      0,      1]])

        def z(self, t):
            return np.matrix([
                [1,         0,      0,      0],
                [0,         1,      0,      0],
                [0,         0,      1,      0],
                [0,         0,      t,      1]])


def v2m(vec):
    return np.matrix([
        [1,      0,      0,      0],
        [0,      1,      0,      0],
        [0,      0,      1,      0],
        [vec[0], vec[1], vec[2], 1]])

def camera_matrix(bounds, heading, tilt, fov, dist):
    # convert bounds to numpy array
    bounds = np.array([[bounds.min.x, bounds.min.y, bounds.min.z], [bounds.max.x, bounds.max.y, bounds.max.z]])
    transform = xform()
    translate = transform.trans()
    rotate = transform.rot()

    # define the pan/tilt angles and solve the transform matrices
    matrix_tilt = rotate.x(np.radians(tilt))
    matrix_heading = rotate.y(np.radians(heading))

    # compose the rotational transform
    matrix_rotation = np.matmul(matrix_tilt, matrix_heading)

    # solve the z position from the diagonal distance of bounds
    height = np.abs(np.linalg.norm(bounds[0] - bounds[1]))
    position = (height / 2) / np.tan(np.radians(fov / 2)) + dist

    # solve the center of the bounds
    center = np.multiply(np.add(bounds[0],bounds[1]),0.5)
    # translation matrix to center
    matrix_center = v2m(center)

    # define the translation matrix along z
    matrix_translate = translate.z(position)

    # solve the cameras transform matrix
    matrix_transform = np.matmul(np.matmul(matrix_translate, matrix_rotation),matrix_center)

    # return the matrix
    return matrix_transform

