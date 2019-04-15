
from arnold import *
from getBounds import getBounds
from xform import rot, trans, cameraMatrix
import os

class Thumbnail:
    def __init__(self, source=None, light=".lights.ass", target="thumbnail.jpeg", pan=45, tilt=45, fov=10, res=512, dist=1, quality = 4, overscan=1):
        test = True
        universe = AiUniverse()

        #Create options
        opt = AiNode(universe, "options")
        AiNodeSetStr(opt, "outputs", "RGBA RGBA /filter /driver")
        AiNodeSetInt(opt, "xres", int(res))
        AiNodeSetInt(opt, "yres", int(res))
        AiNodeSetInt(opt, "AA_samples", quality)

        #Create filter
        filter = AiNode(universe,"gaussian_filter")
        AiNodeSetStr(filter, "name", "/filter")
        AiNodeSetFlt(filter, "width", 2.0)

        #set up driver type
        driver_type = "driver_" + os.path.basename(target).split(".")[1]
        #Create driver
        driver = AiNode(universe, driver_type)
        AiNodeSetStr(driver, "name", "/driver")
        AiNodeSetStr(driver, "filename", target)
        AiNodeSetStr(driver, "colorspace", "auto")

        # create the procedural node for the asset
        asset = AiNode(universe, "procedural")
        AiNodeSetStr(asset, "name", "/asset")
        AiNodeSetStr(asset, "filename", source)
        AiNodeSetBool(asset, "load_at_init", True)

        # write the thumbnail ass file and calculate the bounds
        AiASSWrite(universe, ".thumb.ass", AI_NODE_SHAPE, False, False)
        bounds = getBounds(".thumb.ass")

        #calculate the camera matrix and convert into an AtMatrix
        m = cameraMatrix(bounds,pan,tilt,fov,dist)

        camera_matrix = AtMatrix(m.item(0, 0), m.item(0, 1), m.item(0, 2), m.item(0, 3),
                        m.item(1, 0), m.item(1, 1), m.item(1, 2), m.item(1, 3),
                        m.item(2, 0), m.item(2, 1), m.item(2, 2), m.item(2, 3),
                        m.item(3, 0), m.item(3, 1), m.item(3, 2), m.item(3, 3))

        #create the camera node
        camera = AiNode(universe, "persp_camera")
        AiNodeSetStr(camera, "name", "/Camera")
        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)
        AiArraySetMtx(am, 0, camera_matrix)
        AiNodeSetArray(camera, "matrix", am)
        AiNodeSetFlt(camera, "fov", fov)
        AiNodeSetVec2(camera, "screen_window_min", -overscan, -overscan)
        AiNodeSetVec2(camera, "screen_window_max", overscan, overscan)

        # create the procedural node for the light rig
        asset = AiNode(universe, "procedural")
        AiNodeSetStr(asset, "name", "/light_rig")
        AiNodeSetStr(asset, "filename", light)
        AiNodeSetBool(asset, "load_at_init", True)

        self.test = test
        self.source = source
        self.overscan = overscan
        self.driver = driver
        self.res = res

        self.bounds = bounds

        self.universe = universe

        AiASSWrite(self.universe, ".thumb.ass", AI_NODE_ALL, False, False)

    def export(self, target=None):
        return self.test

    def render(self):
        AiASSLoad(".thumb.ass", AI_NODE_ALL)
        AiRender(AI_RENDER_MODE_CAMERA)