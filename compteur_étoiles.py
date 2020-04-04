import cv2
import numpy
import math
from common import morpho, strel, utils


im = cv2.imread('./Images/etoiles.png', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('Etoile', im)

masque = numpy.zeros(im.shape, im.dtype)
masque[im >= 50] = im[im >= 50] - 50
# cv2.imshow('Masque', masque)

hmax = morpho.reconstruction_inferieure(im, masque, strel.build('carre', 1))
# cv2.imshow('Hmax', hmax)

# On reduit la luminosite de cette maniere
r = im - hmax
# cv2.imshow('r', r)

r[r < 3] = 0
r[r >= 3] = r[r >= 3] - 3
cv2.imshow('Sommets', r)

hmax2 = morpho.reconstruction_inferieure(im-hmax, r, strel.build('carre', 1))
# cv2.imshow('hmax2', hmax2)

s = utils.seuil(hmax2, 47)
cv2.imshow('Sommets seuil', s)
cv2.waitKey(0)

# On creer une ligne verticale et une horizontale
lv = strel.build('ligne', 5, 90)
lh = strel.build('ligne', 5, 0)

# Les dilatation vont remplacer chaque pixel blanc par une ligne (horizontal et vertical pour faire une croix)
s = numpy.maximum(morpho.dilatation(s, lv), morpho.dilatation(s, lh))
cv2.imshow('Sommets seuil croix', s)

imc = cv2.imread('./Images/etoiles.png')
# On passe tout en rouge
imc[s > 0] = [0, 0, 255]
cv2.imshow('Image colore', imc)

cv2.waitKey(0)