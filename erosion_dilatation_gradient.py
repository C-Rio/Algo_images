import cv2
import numpy as np
from common import strel
from common import morpho as m


# def erosion(img, taille=1):
#     (hauteur, largeur) = (img.shape[0], img.shape[1])
#     img2 = np.zeros(img.shape, np.uint8)
#     for i in range (taille, hauteur-taille):
#         for j in range(taille, largeur-taille):
#             img2[i,j] = np.min(img[i-taille:i+taille+1, j-taille:j+taille+1])
#     return img2

# def dilatation(img, taille=1):
#     (hauteur, largeur) = (img.shape[0], img.shape[1])
#     img2 = np.zeros(img.shape, np.uint8)
#     for i in range(taille, hauteur-taille):
#         for j in range (taille, largeur-taille):
#             img2[i, j] = np.max(img[i-taille:i+taille+1, j-taille:j+taille+1])
#     return img2


pragma_8 = strel.build('carre', 1)
# cv2.imshow('Pragma 8', pragma_8)

pragma_4 = strel.build('diamant', 1)
# cv2.imshow('Pragma 4', pragma_4)


img = cv2.imread('./Images/chien.png', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('chien.png', img)
cv2.imshow('Erosion', m.erosion(img, strel.build('diamant', 5)))
cv2.imshow('Dilatation', m.dilatation(img, strel.build('diamant', 5)))


imgVoit = cv2.imread('./Images/voiture.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Voiture', imgVoit)

e1 = strel.build('carre', 1)
e2 = strel.build('ligne', 20, 45)
imgVoitGrad = m.gradient(imgVoit, e1)

cv2.imshow('Gradient', imgVoitGrad)
cv2.waitKey(0)