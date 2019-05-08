from arnold import AiASSLoad, AiASSWrite, AiRender, AI_RENDER_MODE_CAMERA, AI_NODE_ALL
from os import path, chdir

from createUniverse import CreateUniverse


class Thumbnail:
    def __init__(self):
        self.params = dict(
            paths=dict(
                source=dict(
                    path=None,
                    parent=None,
                    name=None
                ),
                target=dict(
                    path=None,
                    parent=None,
                    name=None
                ),
                assfile=dict(
                    path=None,
                    parent=None,
                    name=None
                ),
                light=dict(
                    path=path.abspath(".lights.ass"),
                )
            ),
            universe=dict(
                options=dict(
                    resolution=512,
                    quality=6
                ),
                driver=dict(
                    file_type="jpeg"
                ),
                filter=dict(
                    width=2
                ),
                asset=dict(

                ),
                light=dict(

                ),
                camera=dict(
                    fov=10,
                    azimuth=45,
                    zenith=45,
                    position=0,
                    overscan=1
                )
            )
        )

    def create(self):
        chdir(path.abspath(self.params['paths']['source']['parent']))
        universe = CreateUniverse(self.params['paths'])
        universe.options(self.params['universe']['options'])
        universe.filter(self.params['universe']['filter'])
        universe.driver(self.params['universe']['driver'])
        universe.asset(self.params['universe']['asset'])
        universe.camera(self.params['universe']['camera'])
        universe.lights(self.params['universe']['light'])

        AiASSWrite(universe.universe, self.params['paths']['assfile']['path'], AI_NODE_ALL, False, False)

        return True

    def export(self, target=None):
        return True

    def render(self, target=None):
        thumb_path = target if target else self.params['paths']['assfile']['path']

        AiASSLoad(thumb_path, AI_NODE_ALL)
        AiRender(AI_RENDER_MODE_CAMERA)

        return True
