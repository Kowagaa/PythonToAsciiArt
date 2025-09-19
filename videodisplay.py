import asciiartgen as aag
import av
import os
import numpy as np
import PIL
import time
import tqdm

path = os.path.join("colonthree.mov") #FIle to view
v = av.open(path)
x = 0
texts = ["" for frame in v.decode() if type(frame) is av.VideoFrame]
v = av.open(path)
for frame in tqdm.tqdm(v.decode(), "Fetching images from video/gif"):
    if type(frame) is av.VideoFrame:
        img = frame.to_image()
        texts[x] = aag.printimage((96, 96), #Edit this tuple to set resolution
                                   pilmage= img)
        x+= 1
input("Press enter to view")


for text in texts:
    print(text)
    time.sleep(0.02)
