import cv2
import numpy
from common import morpho, strel, utils

# Image de base
img = cv2.imread('./exo2/feuille1.png', cv2.IMREAD_COLOR)
cv2.imshow('img', img)

el = strel.build('disque', 4)

# image avec seulement le canal 1
img_c1 = img[:, :, 1]
cv2.imshow('img_c1', img_c1)

#On fait une fermeture pour recuperer le fond
ferm = morpho.fermeture(img_c1, el)
cv2.imshow('Fond', ferm)

#On retire le fond de l'image
img_sans_fond = ferm - img_c1
cv2.imshow('img_sans_fond', img_sans_fond)

cv2.waitKey(0)
