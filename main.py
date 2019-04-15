import thumb
import os
from os import path
from arnold import *


source=path.abspath("/home/shawn/gaffer/projects/default/asses/2D_test/basket.ass")
light=path.abspath(".lights.ass")
print path.exists(source)

target="thumbnail.jpeg"
pan=45
tilt=45
fov=10
res=512
dist = 1
quality = 6
overscan=1

AiBegin()
myThumbnail = thumb.Thumbnail(source,light,target,pan,tilt,fov,res,dist,quality,overscan)
myThumbnail.render()
AiEnd()

print myThumbnail.bounds.min.x