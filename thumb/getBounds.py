from arnold import *

def getBounds(source):

    AiASSLoad(source, AI_NODE_SHAPE)
    AiRender(AI_RENDER_MODE_FREE)
    bounds = AiUniverseGetSceneBounds()
    AiRenderEnd()


    return bounds