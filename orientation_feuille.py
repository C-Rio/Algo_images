import cv2
import numpy as np
from common import strel
from common import morpho as m


img = cv2.imread('./Images/papier_15.png')
# Canal rouge car feuille verte et ressort mieux :
imgB = img[:, :, 0] #On conserve le canal bleu
cv2.imshow('Feuille B', imgB)
imgV = img[:, :, 1] #On conserve le canal vert
cv2.imshow('Feuille V', imgV)
imgR = img[:, :, 2] #On conserve le canal rouge
cv2.imshow('Feuille R', imgR)
cv2.waitKey(0)
cv2.destroyAllWindows()

img = imgR

#On cherche a reduire au max le nombre de pixel blanc car moins il y a de pixels et plus ont se rapproche de l'angle recherche
min = np.sum(img)
angle = 0
for a in range (-90, 90, 1):
    el = strel.build('ligne', 40, a)
    cv2.imshow('Ligne', el)

    g = m.gradient(img, el)
    cv2.imshow('Calcul', g)
    cv2.waitKey(0)
    if (np.sum(g) < min) :
        min = np.sum(g)
        angle = a

print (angle)



