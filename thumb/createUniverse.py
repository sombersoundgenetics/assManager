from arnold import *
from os import remove


class Bounds:
    def __init__(self,universe):

        AiASSWrite(universe, '.bounds.ass', AI_NODE_SHAPE, False, False)
        AiASSLoad('.bounds.ass', AI_NODE_SHAPE)
        AiRender(AI_RENDER_MODE_FREE)
        self.bounds = AiUniverseGetSceneBounds()
        AiRenderEnd()
        remove('.bounds.ass')


class searchpaths :
    def __init__(self,source):
        texture = None
        procedural = None
        plugin = None
        AiASSLoad(source, AI_NODE_OPTIONS)
        node_iter = AiUniverseGetNodeIterator(AI_NODE_OPTIONS)
        while not AiNodeIteratorFinished(node_iter):
            node = AiNodeIteratorGetNext(node_iter)
            texture = AiNodeGetStr(node, "texture_searchpath")
            procedural = AiNodeGetStr(node, "procedural_searchpath")
            plugin = AiNodeGetStr(node, "plugin_searchpath")
        AiNodeIteratorDestroy(node_iter)

        self.texture = texture
        self.procedural = procedural
        self.plugin = plugin


class CreateUniverse:
    def __init__(self, paths):
        import os
        self.os = os
        self.path = paths
        self.universe = AiUniverse()

    def options(self, params):
        res = params['resolution']
        quality = params['quality']

        self.options = AiNode(self.universe, "options")
        AiNodeSetStr(self.options, "outputs", "RGBA RGBA /filter /driver")
        AiNodeSetInt(self.options, "xres", int(res))
        AiNodeSetInt(self.options, "yres", int(res))
        AiNodeSetInt(self.options, "region_max_x", int(res - 1))
        AiNodeSetInt(self.options, "region_max_y", int(res - 1))
        AiNodeSetInt(self.options, "AA_samples", quality)

        #Copy Searchpaths from source
        searchpath = searchpaths(self.path['source']['path'])
        AiNodeSetStr(self.options, "texture_searchpath", searchpath.texture)
        AiNodeSetStr(self.options, "procedural_searchpath", searchpath.procedural)
        AiNodeSetStr(self.options, "plugin_searchpath", searchpath.plugin)

    def filter(self, params):
        width = params['width']

        # Create filter
        filter = AiNode(self.universe,"gaussian_filter")
        AiNodeSetStr(filter, "name", "/filter")
        AiNodeSetFlt(filter, "width",width)

    def driver(self,params):
        if self.path['target']['path'] is None :
            file_type = params['driver']['file_type']
        else :
            file_type = self.os.path.splitext(self.path['target']['path'])[1]

        target_path = self.path['target']['path']

        # Create driver
        driver = AiNode(self.universe, "driver_" + file_type.split(".")[1])
        AiNodeSetStr(driver, "name", "/driver")
        AiNodeSetStr(driver, "filename", target_path)
        AiNodeSetStr(driver, "colorspace", "auto")

    def asset(self,params):
        source = self.path['source']['path']

        # create the procedural node for the asset
        asset = AiNode(self.universe, "procedural")
        AiNodeSetStr(asset, "name", "/asset")
        AiNodeSetStr(asset, "filename", source)
        AiNodeSetBool(asset, "load_at_init", True)

    def camera(self,params):
        from xform import camera_matrix

        fov = params['fov']
        overscan = params['overscan']

        # calculate the camera matrix and convert into an AtMatrix
        bounds = Bounds(self.universe)

        m = camera_matrix(bounds.bounds, params['azimuth'], params['zenith'], params['fov'], params['position'])

        camera_matrix = AtMatrix(m.item(0, 0), m.item(0, 1), m.item(0, 2), m.item(0, 3),
                                 m.item(1, 0), m.item(1, 1), m.item(1, 2), m.item(1, 3),
                                 m.item(2, 0), m.item(2, 1), m.item(2, 2), m.item(2, 3),
                                 m.item(3, 0), m.item(3, 1), m.item(3, 2), m.item(3, 3))

        # create the camera node
        camera = AiNode(self.universe, "persp_camera")
        AiNodeSetStr(camera, "name", "/Camera")
        am = AiArrayAllocate(1, 1, AI_TYPE_MATRIX)
        AiArraySetMtx(am, 0, camera_matrix)
        AiNodeSetArray(camera, "matrix", am)
        AiNodeSetFlt(camera, "fov", fov)
        AiNodeSetVec2(camera, "screen_window_min", -overscan, -overscan)
        AiNodeSetVec2(camera, "screen_window_max", overscan, overscan)

    def lights(self, params):
        # create the procedural node for the light rig
        light = self.path['light']['path']
        asset = AiNode(self.universe, "procedural")
        AiNodeSetStr(asset, "name", "/light_rig")
        AiNodeSetStr(asset, "filename", str(light))
