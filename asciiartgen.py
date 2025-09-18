import numpy as np
import skimage as ski
import os
from PIL import Image

from enum import Enum
class background(Enum):
    OPAQUE = "███"

    TRANSLUICD_OPAQUE = "▓▓▓"
    
    TRANSLUCID = "▒▒▒"

    TRASPARENT =  "░░░"
    
    OFF = "   "

background_list = [background.OPAQUE, background.TRANSLUICD_OPAQUE, background.TRANSLUCID, background.TRASPARENT, background.OFF]
 
filename = os.path.join('colonthree.bmp') #Image to display
pilmage = Image.open(filename)

pilmage.thumbnail((64, 64)) #Resolution of the text 

filename2 = os.path.join('out.bmp')

pilmage.save(filename2)

image = ski.io.imread(filename2)



text = ""
start = "\033[107m"
end = "\033[0m"

huetranslator = [1, 3, 2, 6, 4, 5]

class Pixel:
    def __init__(self, hue : int, saturation : int, value : int):
        self.hue = hue
        self.saturation = saturation
        self.value = value
    def skiPixelToPixel(self, hsv_values):
        self.hue = int(hsv_values[0]*5.0+1.0)
        self.saturation = int(hsv_values[1]*2.0+0.5)
        self.value = int(hsv_values[2]*4.0+0.5)
    def pixelToText(self):
        global background_list
        match huetranslator[self.hue]:
            case 1:
                if self.saturation > 1:
                    _text = "\033[91m"
                else:
                    _text = "\033[31m"
            case 2:
                if self.saturation > 1:
                    _text = "\033[92m"
                else:
                    _text = "\033[32m"
            case 3:
                if self.saturation > 1:
                    _text = "\033[93m"
                else:
                    _text = "\033[33m"
            case 4:
                if self.saturation > 1:
                    _text = "\033[94m"
                else:
                    _text = "\033[34m"
            case 5:
                if self.saturation > 1:
                    _text = "\033[95m"
                else:
                    _text = "\033[35m"
            case 6:
                if self.saturation > 1:
                    _text = "\033[96m"
                else:
                    _text = "\033[36m"
        if self.saturation == 0:
            _text = "\033[30m"
        _text += background_list[self.value].value
        return _text


print(ski.color.rgb2hsv(np.array(image[0,1][:3],dtype=np.uint8)))
shape = np.shape(image)
pixelarr = np.array([[Pixel(0,0,0) for i in range(shape[1])] for j in range(shape[0])])
for i in range(shape[0]):
    for j in range(shape[1]):
        pixelarr[i, j].skiPixelToPixel(ski.color.rgb2hsv(np.array(image[i, j][:3],dtype=np.uint8)))

text += start
for i in range(shape[0]):
    for j in range(shape[1]):
        text += pixelarr[i, j].pixelToText()
    text += "\n"
text += end




print(text)
