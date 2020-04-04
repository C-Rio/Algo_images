import cv2
import numpy
from common import morpho, strel, utils

img = cv2.imread('./Images/SaltPepper.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('SaltPepper', img)

ligneVertical = strel.build('ligne', 3, 90)
# cv2.imshow('Ligne vetical', ligne1)

#Nous permet de recup les carres blanc et bande blanches
fe = morpho.fermeture(img, ligneVertical)
cv2.imshow('Fermeture vetical', fe)

#Pareil
ligneHorizontal = strel.build('ligne', 2, 0)
fe2 = morpho.fermeture(img, ligneHorizontal)
cv2.imshow('Fermeture horizontal', fe2)

#On recupere un max de gris => plus de poivre a ce moment
min = numpy.minimum(fe, fe2)
cv2.imshow('Minimum', min)

#L'ouverture va permettre de "boucher" les trou blanc
ligneVertical2 = strel.build('ligne', 5, 90)
ouv = morpho.ouverture(min, ligneVertical2)
cv2.imshow('Ouverture vertical', ouv)

#La fermeture va permettre de supprimer les pixels noir parmis les carres et bande blanc
fe3 = morpho.fermeture(ouv, ligneVertical)
cv2.imshow('Suppression bruit', fe3)

cv2.waitKey(0)