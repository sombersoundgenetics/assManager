
from arnold import *
from getBounds import getBounds
from xform import rot, trans, cameraMatrix
import os, sys
import subprocess


class Thumbnail:
    def __init__(self, source=None, light=".lights.ass", target="thumbnail.jpeg", pan=45, tilt=45, fov=10, res=512, dist=1, quality = 4, overscan=1):
        test = True


        texture_searchpath = ""
        procedural_searchpath = ""
        plugin_searchpath = ""

        source_path = os.path.split(source)[0]
        source_file = os.path.split(source)[1]
        source_name = os.path.splitext(source_file)[0]

        thumb_file = source_name + ".thumb.ass"
        thumb_path = os.path.join(source_path,thumb_file)

        AiASSLoad(source, AI_NODE_OPTIONS)
        iter = AiUniverseGetNodeIterator(AI_NODE_OPTIONS)
        while not AiNodeIteratorFinished(iter):
            node = AiNodeIteratorGetNext(iter)
            texture_searchpath = AiNodeGetStr(node, "texture_searchpath")
            procedural_searchpath = AiNodeGetStr(node, "procedural_searchpath")
            plugin_searchpath = AiNodeGetStr(node, "plugin_searchpath")
        AiNodeIteratorDestroy(iter)

        AiUniverseCacheFlush(AI_NODE_ALL)

        init_univ = AiMalloc(1024)
        #create universe
        universe = AiUniverse()

        #Create options
        opt = AiNode(universe, "options")
        AiNodeSetStr(opt, "outputs", "RGBA RGBA /filter /driver")
        AiNodeSetInt(opt, "xres", int(res))
        AiNodeSetInt(opt, "yres", int(res))
        AiNodeSetInt(opt, "region_max_x", int(res-1))
        AiNodeSetInt(opt, "region_max_y", int(res-1))
        AiNodeSetInt(opt, "AA_samples", quality)

        #Copy Searchpaths from source
        AiNodeSetStr(opt, "texture_searchpath", texture_searchpath)
        AiNodeSetStr(opt, "procedural_searchpath", procedural_searchpath)
        AiNodeSetStr(opt, "plugin_searchpath", plugin_searchpath)

        #Create filter
        filter = AiNode(universe,"gaussian_filter")
        AiNodeSetStr(filter, "name", "/filter")
        AiNodeSetFlt(filter, "width", 2.0)

        #set up driver type
        file_type = os.path.basename(target).split(".")[1]
        driver_type = "driver_" + file_type
        target_file = os.path.join(source_path,source_name + ".thumb." + file_type)

        #Create driver
        driver = AiNode(universe, driver_type)
        AiNodeSetStr(driver, "name", "/driver")
        AiNodeSetStr(driver, "filename", target_file)
        AiNodeSetStr(driver, "colorspace", "auto")

        # create the procedural node for the asset
        asset = AiNode(universe, "procedural")
        AiNodeSetStr(asset, "name", "/asset")
        AiNodeSetStr(asset, "filename", source)
        AiNodeSetBool(asset, "load_at_init", True)

        # write the thumbnail ass file and calculate the bounds
        AiASSWrite(universe, thumb_path, AI_NODE_SHAPE, False, False)
        bounds = getBounds(thumb_path)

        # create the procedural node for the light rig
        asset = AiNode(universe, "procedural")
        AiNodeSetStr(asset, "name", "/light_rig")
        AiNodeSetStr(asset, "filename", light)

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

        AiASSWrite(universe, thumb_path, AI_NODE_ALL, False, False)


        self.test = test
        self.source = os.path.abspath(source)
        self.thumb_path = os.path.abspath(thumb_path)
        self.thumb_file = thumb_file
        self.overscan = overscan
        self.driver = driver
        self.res = res
        self.source_path = source_path

        self.bounds = bounds

        self.universe = universe

    def export(self, target=None):
        return self.test

    def render(self,kick="kick"):

        thumb_path = self.thumb_path

        AiUniverseCacheFlush(AI_NODE_ALL)
        AiASSLoad(thumb_path, AI_NODE_ALL)

        AiRender(AI_RENDER_MODE_CAMERA)

        return True
