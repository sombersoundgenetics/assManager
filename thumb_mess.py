

from arnold import *
import os.path as path
import numpy as np


def rot(t, axis):

    #solve sin and cosine of theta
    cost = np.cos(t)
    sint = np.sin(t)

    #solve rotations along x
    if axis == 0 or axis is "x":
        mi = np.matrix([
            [1,         0,      0,      0],
            [0,         cost,   -sint,  0],
            [0,         sint,   cost,   0],
            [0,         0,      0,      1]])
    #solve rotations around y
    elif axis == 1 or axis is "y":
        mi = np.matrix([
            [cost,      0,      sint,   0],
            [0,         1,      0,      0],
            [-sint,     0,      cost,   0],
            [0,         0,      0,      1]])
    #solve rotations around z
    elif axis == 2 or axis is "z":
        mi = np.matrix([
            [cost,      -sint,  0,      0],
            [sint,      cost,   0,      0],
            [0,         0,      1,      0],
            [0,         0,      0,      1]])
    #return identity matrix as default
    else:
        mi = np.matrix([
            [1,         0,      0,      0],
            [0,         1,      0,      0],
            [0,         0,      1,      0],
            [0,         0,      0,      1]])


    #return the matrix
    return mi


class Thumb:

    #load the ass file and start the renderer
    def __init__(self, myass, pan = 45, tilt = 45, fov = 50):
        self.myass = myass
        self.pan = pan
        self.tilt = tilt
        self.fov = fov

        AiASSLoad(self.myass, AI_NODE_SHAPE)

        nodeIter = AiUniverseGetNodeIterator(AI_NODE_SHAPE)
        self.shapes = []
        while not AiNodeIteratorFinished(nodeIter):
            self.shapes.append(AiNodeIteratorGetNext(nodeIter))
        AiNodeIteratorDestroy(nodeIter)

        AiRender(AI_RENDER_MODE_FREE)

        bounds = AiUniverseGetSceneBounds()
        self.bounds = bounds

        AiRenderAbort()

        # convert arnold bounds to numpy array
        bounds = np.array([[bounds.min.x, bounds.min.y, bounds.min.z], [bounds.max.x, bounds.max.y, bounds.max.z]])

        # define the pan/tilt angles and solve the transform matrices
        mRx = rot(np.radians(tilt), 0)
        mRy = rot(np.radians(pan), 1)

        # compose the rotational transform
        mR = np.matmul(mRx, mRy)

        # solve the z position from the diagonal distance of bounds
        h = np.abs(np.linalg.norm(bounds[0] - bounds[1]))
        z = h / (np.tan(np.radians(fov) / 2))

        # apply to z position to the translate matrix
        mT = np.matrix([
            [1,     0,      0,      0],
            [0,     1,      0,      0],
            [0,     0,      1,      0],
            [0,     0,      z,      1]])

        # solve the cameras transform
        m = np.matmul(mT, mR)

        self.camera_matrix = AtMatrix(m.item(0, 0), m.item(0, 1), m.item(0, 2), m.item(0, 3),
                        m.item(1, 0), m.item(1, 1), m.item(1, 2), m.item(1, 3),
                        m.item(2, 0), m.item(2, 1), m.item(2, 2), m.item(2, 3),
                        m.item(3, 0), m.item(3, 1), m.item(3, 2), m.item(3, 3))


        self.universe = AiUniverse()



    #Define a new camera and place according to scene bounds
    #TODO add options, drivers nodes
    #TODO reference ass file as procedural, write new file and load it instead (rather than copying the entire thing)
    def setup(self):

        # make a camera node
        camera = AiNode(self.universe, "persp_camera")
        # define the camera's properties
        AiNodeSetStr(camera, "name", "/Camera")
        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)
        AiArraySetMtx(am, 0, self.camera_matrix)
        AiNodeSetArray(camera, "matrix", am)
        AiNodeSetFlt(camera, "fov", self.fov)

        AiASSWrite(self.universe, "thumb.ass", AI_NODE_ALL, True, False)

        return

    #write the ass file for the thumb
    #TODO Cleanup file, delete other cameras
    def write(self,path):
        AiASSWrite(self.universe,path, AI_NODE_ALL, True, False)
        return

    #Render the thumb
    def render(self):
        return

#myass = path.abspath("/home/shawn/gaffer/projects/default/asses/test/test.0001.ass")


myass = path.abspath("/home/shawn/Downloads/cube.ass")
pan = 45.
tilt = 45.
fov = 50.

#TODO check if thumb ass file exists and render it instead
if path.exists(myass) :

    AiBegin()
    mythumb = Thumb(myass, -30, 20, 24)
    mythumb.setup()
    newpath = path.join(path.dirname(myass), "everything.ass")
    mythumb.write(newpath)
    AiEnd()
else:
    print "!!!"