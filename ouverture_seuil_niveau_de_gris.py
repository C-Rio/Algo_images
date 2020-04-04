import cv2
import numpy as np
from common import utils

# Ouvrir image en niveau de gris
img = cv2.imread('./images/toulouse.jpg', cv2.IMREAD_GRAYSCALE)

print img.shape
hauteur = img.shape[0]
largeur = img.shape[1]
print 'largeur =', largeur, 'hauteur =', hauteur

# Tous les pixel < 60 passent a 0 et tous ceux >= 60 passent a 255
seuil = utils.seuil(img, 60)

cv2.imshow('Mon beau chat N&B seuil', seuil)


# Ouvrir image en couleur
imgCoul = cv2.imread('./images/toulouse.jpg')

# modification pixels

#On met a 0 (noir) les 100 premieres ligne sur toutes les colonnes
imgCoul[0:100, :] = 0

#On met a 0 (noir) les 100 premieres colonnes sur toutes les lignes
imgCoul[:, 0:100] = 0

#On met en gris les lignes 100 a 110 sur toutes les colonnes
imgCoul[100:110, :] = [200, 200, 200] #[bleu, vert, rouge]
#ou
imgCoul[110:115, :] = 255

cv2.imshow('Mon beau chat Coul', imgCoul)


#diagonale
for i in range (0,largeur):
    imgCoul[i:i+10, i:i+10] = [0, 175, 255]

cv2.imshow('Mon beau chat Coul Diag', imgCoul)

#niveaux de gris manuel (fait par cv2.IMREAD_GRAYSCALE
imgCoul = cv2.imread('./images/toulouse.jpg')
img = np.uint8((1.0*imgCoul[:, :, 0] + imgCoul[:, :, 1] + imgCoul[:, :, 2]) /3)
cv2.imshow('Mon beau chat N&B Man', img)


cv2.waitKey(0)




