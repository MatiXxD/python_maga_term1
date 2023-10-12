import cv2
import numpy as np

class Experiment:

    def __init__(self, dct):
        '''Конструктор'''
        self._date = dct["date"]
        self._path = dct["path"]
        self._features = dct["features"]
        self._image = cv2.imread(self._path, 0)
        self._processedImg = self._image
        self._gf = np.array([])
 
    def printInfo(self):
        '''Вывод приватных полей класса'''
        print("Date = ", self._date, "\nPath = ", \
            self._path, "\nFeatures = ", self._features)

    def getData(self):
        '''Вернуть дату создания'''
        return self._date

    def getImageShape(self):
        '''Найти размер изображения'''
        return f"{len(self._image[0])}x{len(self._image)}"

    def _imageNormalization(self, args):
        '''Возвращает нормализованное изображение'''
        return cv2.normalize(self._image, None, alpha=args[0], beta=args[1], norm_type=cv2.NORM_MINMAX)

    def _imageBluring(self, args):
        '''Применяет фильтр Гаусса к изображению'''
        return cv2.GaussianBlur(self._image, args, cv2.BORDER_DEFAULT)

    def _imageProcessing(self, args):
        '''Применяет фильтр Гаусса к нормализованному изображению'''
        self._processedImg = cv2.GaussianBlur(self._imageNormalization(args[0]), args[1], cv2.BORDER_DEFAULT)
        return self._processedImg

    def _createGaborFilter(self, args):
        '''Создать фильтр Габора'''
        return cv2.getGaborKernel((args[0], args[0]), args[1], args[2], args[3], args[4]) 

    def _featureExtraction(self, args):
        '''Применить фильтр Габора к изображению'''
        if self._features == "Gabor":
            kern = self._createGaborFilter(args["Gabor"])
            self._gf = cv2.filter2D(self._image, cv2.CV_8UC3, kern) 
            return self._gf
        else:
            raise Exception("Wrong features")

    def _getFeatureShape(self):
        '''Вернуть вектор признаков и его длину'''
        if len(self._gf) != 0:
            vec = np.array(self._gf).flatten()
            return (vec, len(vec))
        else:
            raise Exception("Use _featureExtraction()") 

