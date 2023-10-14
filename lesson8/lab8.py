from skimage.filters import gabor_kernel
from scipy import ndimage as ndi
import cv2 as cv
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import wfdb
import heartpy as hp
from scipy.signal import find_peaks
from processing import *


##### Signal processing
obj = SignalProcessing("/home/ilya/Study/labsPython/lesson8/ecg.csv")
obj.readSignal("MLII")

obj.visualize()
print(obj.getShape())
obj.plotPeaks()
features = obj.featureExtraction()
for k, v in features.items():
    print(k, v)

cf1 = SignalProcessing.getPredict(obj.featureExtraction(), [[200, 25], [400, 40]])
for k, v in cf1.items():
    print(k, v)


##### Image processing
imgObj = ImageProcessing("chest-xray.tif")
size = imgObj.getShape()
print(size[0], "x", size[1], sep="")

args = {"ksize" : 16, "sigma" : 2, "theta" : np.pi / 2, "lambda" : 0.3, "gamma" : 1.0}
features = imgObj.featureExtraction(args)
for k, v in features.items():
    print(k, v)

images = imgObj.getImages()
for k, v in images.items():
    imgObj.visualize(k, v)

cf2 = ImageProcessing.getPredict(imgObj.featureExtraction(args), [[2, 15], [4, 40]])
for k, v in cf2.items():
    print(k, v)
