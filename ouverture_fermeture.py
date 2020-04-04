import cv2
import numpy
from common import morpho, strel, utils

img = cv2.imread('./Images/chien.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Chien', img)


el = strel.build('disque', 8)

ouv = morpho.ouverture(img, el)
cv2.imshow('Chien ouverture', ouv)

fe = morpho.fermeture(img, el)
cv2.imshow('Chien fermeture', fe)


#Test idempotence
fe2 = morpho.fermeture(fe, el)

if(numpy.array_equal(fe, fe2)):
    print('Idempotence')

cv2.waitKey(0)

