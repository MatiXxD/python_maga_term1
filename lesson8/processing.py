from skimage.filters import gabor_kernel 
from scipy import ndimage as ndi 
import cv2 as cv 
import matplotlib.pyplot as plt 
from scipy.ndimage.filters import gaussian_filter 
from matplotlib import pyplot as plt 
import numpy as np 
import pandas as pd 
import wfdb 
import heartpy as hp 
from abc import ABC, abstractmethod 
from scipy.signal import find_peaks 
 


class BaseProcessing(ABC): 
 
    @abstractmethod 
    def _filtering(self): 
        pass 
 
    @abstractmethod 
    def visualize(self): 
        pass 
 
    @abstractmethod 
    def getShape(self): 
        pass 
 
    @abstractmethod 
    def featureExtraction(self): 
        pass 

    @staticmethod
    def getPredict(features, etalons):
        c0 = ((features["mean"] - etalons[0][0])**2 + (features["std"] - etalons[0][1])**2)**(1/2)
        c1 = ((features["mean"] - etalons[1][0])**2 + (features["std"] - etalons[1][1])**2)**(1/2)

        if c0 < c1:
            return {"features" : etalons[0], "class" : 0}
        else:
            return {"features" : etalons[1], "class" : 1}
 

class SignalProcessing(BaseProcessing): 
 
    def __init__(self, path): 
        self.selectData(path)

    ############################################

    def _filtering(self):
        if self._signal is None: raise Exception("Signal is None")
        return hp.filter_signal(self._signal, cutoff = [0.75, 3.5], 
                                sample_rate = 100, order = 3, filtertype = "bandpass")
     
    def _signalFindPeaks(self, showPlt):
        filtered = self._filtering()
        peaks, _ = find_peaks(filtered, height = 20)

        if showPlt:
            plt.plot(filtered, "blue")
            plt.plot(peaks, filtered[peaks], 'o', color="orange")
            plt.show()
        
        return peaks


    def _calculate_RR_intervals(self):
        peaks = self._signalFindPeaks(0)
        return np.diff(peaks)

    ############################################

    def selectData(self, path):
        self._data = pd.read_csv(path) 
        self._signal = None

    def readSignal(self, str):
        self._signal = self._data[str]

    def visualize(self):
        if self._signal is None: raise Exception("Signal is None")
        plt.plot(self._signal)  
        plt.show() 
 
    def plotPeaks(self):
        self._signalFindPeaks(1)

    def getShape(self): 
        return (self._signal.shape)[0] 

    def featureExtraction(self): 
        rr = self._calculate_RR_intervals()
        features = dict()
        
        features["min"] = np.min(rr)
        features["max"] = np.max(rr)
        features["mean"] = np.mean(rr)
        features["std"] = np.std(rr)

        return features


class ImageProcessing(BaseProcessing):

    def __init__(self, path):
        self.selectImage(path)
        
    ############################################

    def _filtering(self):
        return cv.GaussianBlur(self._image, args, cv.BORDER_DEFAULT)

    def _createGaborFilter(self, args):
        return cv.getGaborKernel((args["ksize"], args["ksize"]), 
                                  args["sigma"], args["theta"], 
                                  args["lambda"], args["gamma"])

    def _useGaborFilter(self, kern):
        self._processed = cv.filter2D(self._image, cv.CV_8UC3, kern)

    ############################################

    def selectImage(self, path):
        self._image = cv.imread(path, 0)
        self._processed = self._image

    def getImages(self):
        return {"origin" : self._image, "processed" : self._processed}

    def visualize(self, title, image):
        cv.imshow(title, image)
        cv.waitKey()

    def getShape(self):
        return np.array([len(self._image[0]), len(self._image)])

    def featureExtraction(self, args):
        self._useGaborFilter(self._createGaborFilter(args))
        temp = np.array(self._processed); temp = temp.flatten()
        return {"mean" : np.mean(temp), "std" : np.std(temp)}