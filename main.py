import thumb
import os
from os import path
from arnold import *

source=path.abspath("/home/shawn/Documents/Sombersound Genetics/Jobs/models/furnishing/midcentury/basket/ass/basket.ass")
light=path.abspath(".lights.ass")

target="thumbnail.jpeg"
pan=65
tilt=30
fov=10
res=1024
dist = 1
quality = 6
overscan=1

os.chdir(os.path.split(source)[0])
AiBegin()
myThumbnail = thumb.Thumbnail(source,light,target,pan,tilt,fov,res,dist,quality,overscan)
myThumbnail.render()
AiEnd()

