import cv2
from experiment import Experiment

dct = {"date" : "07.10.2023", "path" : "/home/ilya/Study/labsPython/lesson7/img.jpg", "features" : "Gabor"}
testObj = Experiment(dct)
#testObj.printInfo()

print("\nDate is", testObj.getData())
print("\nImage size is", testObj.getImageShape())

#cv2.imshow("Normalized image", testObj._imageNormalization([100, 200]))
#cv2.imshow("Smoothing image", testObj._imageBluring((5, 5)))
#cv2.imshow("Processing image", testObj._imageProcessing([[100, 200], (5, 5)]))
#cv2.imshow("Gabor filter", testObj._createGaborFilter([31, 25, 0, 0.3, 0]))

testObj._imageProcessing([[100, 200], (5, 5)])
imgFiltered = testObj._featureExtraction({"Gabor" : [16, 2, 0, 0.3, 0]})
cv2.imshow("Using gabor filter", imgFiltered)
cv2.waitKey()

try:
    vec, l = testObj._getFeatureShape()
    print(vec, l, sep="\n")
except Exception as err:
    print(err)

