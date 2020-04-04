import cv2
import numpy
from common import morpho, strel, utils

img = cv2.imread('./Images/aeroport2.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Aeroport', img)

tmp = numpy.ones(img.shape, img.dtype)*255
cv2.imshow('Image blanche', tmp)

for angle in range (-90, 90):
    el = strel.build('ligne', 40, angle)
    #Quand une ligne sera parallèle avec une piste, la piste ressortira plus en noir
    g = morpho.fermeture(img, el)
    #On garde les pixel les plus sombre pour garder les piste dans tmp
    tmp = numpy.minimum(tmp, g)
    # cv2.imshow('Pistes', tmp)
    # cv2.waitKey(0)

#On seuil pour ne garder que les piste dans tmp
s = utils.seuil(tmp, 30)
cv2.imshow('Pistes', tmp)

#On fait une ouverture pour boucher les traits blancs sur les pistes
ouv = morpho.ouverture(s, strel.build('diamant', 1))
cv2.imshow('Ouverture', ouv)

#On fait un gradient pour recup les contours des pistes
bord = morpho.gradient(s, strel.build('diamant', 1))
cv2.imshow('Gradient', bord)

im = cv2.imread('./Images/aeroport2.png')
b = im[:, :, 0]
v = im[:, :, 1]
r = im[:, :, 2]

#Les pixels qui sont blanc (contours) sont mis en rouge uniquement
r[bord>0] = 255
b[bord>0] = 0
v[bord>0] = 0

#On peut egalement faire ca au lieu de la ligne 33 a 40
# im[bord>0] = [0, 0, 255]

cv2.imshow('Aeroport2', im)

cv2.waitKey(0)