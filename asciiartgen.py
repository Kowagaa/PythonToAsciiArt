import numpy as np
import skimage as ski
import os
from PIL import Image
from enum import Enum

class NoInputProvidedError(Exception):
    def __init__(self, msg):
        super().__init__(f"No arguments provided, please provide {msg}")

class ProvidedPathAndNumpyArrayError(Exception):
    def __init__(self, path):
        super().__init__(f"Provided Both path {path} for image and a numpy array when only one must be input")



class background(Enum):
    OPAQUE = "███"

    TRANSLUICD_OPAQUE = "▓▓▓"
    
    TRANSLUCID = "▒▒▒"

    TRASPARENT =  "░░░"
    
    OFF = "   "

background_list = [background.OPAQUE, background.TRANSLUICD_OPAQUE, background.TRANSLUCID, background.TRASPARENT, background.OFF]
 


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

def printimage(dimensions : tuple[int],path= None, pilmage= None):
    """
    Only Input either path or numpy image
    """
    global background_list
    global start
    global end
    global huetranslator
    text = ""
    if path != None and pilmage != None:
        raise ProvidedPathAndNumpyArrayError(path= path)
    if path != None:
        pilmage = Image.open(os.path.join(path))
        
    elif pilmage != None:
        pass
    
    else:
        raise NoInputProvidedError(msg= "either a path or numpy image")
    pilmage.thumbnail(dimensions) #Resolution of the text 
    image = np.asarray(pilmage)
    
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


    return text
