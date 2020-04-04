import cv2
import numpy
from common import morpho, strel, utils


def seuil_otsu(im):
    var_min = numpy.var(im)*len(im[im>=0])
    best_seuil=0

    for s in range(1, 255):
        #Groupe 1 : pixels <s
        card_G1 = len(im[im<s])
        card_G2 = len(im[im>=s])



        if(card_G1 >0 and card_G2>0):
            var_G1 = numpy.var(im[im<s])
            var_G2 = numpy.var(im[im>=s])



            var_intra = card_G1*var_G1 + card_G2*var_G2

            if(var_intra < var_min):
                var_min = var_intra
                best_seuil = s

    return best_seuil


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


# On cherche le seuil optimal
seuil_opti = seuil_otsu(img_sans_fond)

#On applique un seuil pour faire ressortir le texte
img_seuil = utils.seuil(img_sans_fond, seuil_opti)
cv2.imshow('img_seuil', img_seuil)

el = strel.build('ligne', 40, -90)
max = numpy.sum(morpho.ouverture(img_seuil, el))
angle = -90
for a in range (-90, 90, 1):
    el = strel.build('ligne', 40, a)
    g = morpho.ouverture(img_seuil, el)
    if (numpy.sum(g) > max) :
        max = numpy.sum(g)
        angle = a

print "Angle :", angle

# lignes principales
el = strel.build('ligne', 10, angle)
ligne = morpho.ouverture(img_seuil, el)
cv2.imshow('ligne', ligne)

# Images sans les lignes principales
img_sans_lignes_prin = img_seuil - ligne
cv2.imshow('img_sans_lignes_prin', img_sans_lignes_prin)

cv2.waitKey(0)
