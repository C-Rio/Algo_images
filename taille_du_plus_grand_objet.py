import cv2
import numpy
from common import morpho, strel, utils

img = cv2.imread('./Images/rice.png', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('Rice', img)

el = strel.build('disque', 30)
ouv = morpho.ouverture(img, el)

#On retire d'abord le fond de l'image et on applique un seuil pour faire ressortir les grains de riz
top_hat = img - ouv
s = utils.seuil(top_hat, 60)
s2 = numpy.copy(s)
cv2.imshow('Rice', top_hat)
cv2.waitKey(0)

rayon = 1.0

#On s'arrete quand l'ouv devient totalement noire
while(numpy.max(ouv)>0):
    rayon = rayon + 0.1
    disque = strel.build('disque', rayon)
    #On fait une ouverture sur l'image seuil pour eliminer tous les grains de riz plus petit que le rayon,
    # on update juste l'element structurant a chaque fois
    ouv = morpho.ouverture(s, disque)
    cv2.imshow('Rice', ouv)
    cv2.waitKey(0)
    print (rayon)

taille = (rayon - 0.1) * 2
print (taille)

cv2.waitKey(0)

