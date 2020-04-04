import cv2
import numpy
from common import morpho, strel, utils


img = cv2.imread('./Images/numbers.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Numbers', img)

el = strel.build('disque', 3)
#On fait une ouverture pour recuper le fond
ouv = morpho.ouverture(img, el)
cv2.imshow('Fond', ouv)

#On retire le fond de l'image
top_hat = img - ouv
cv2.imshow('Fond retire', top_hat)

#On applique un seuil pour faire ressortir les chiffres
top_hat = utils.seuil(top_hat, 30)
cv2.imshow('Top hat', top_hat)

cv2.waitKey(0)