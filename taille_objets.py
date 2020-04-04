import cv2
import numpy
import math
from common import morpho, strel, utils


img = cv2.imread('./Images/rice.png', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('Rice', img)

gamma_8 = strel.build('carre', 1)

el = strel.build('disque', 8)
ouv = morpho.ouverture(img, el)

img_seuil = img - ouv
img_seuil = utils.seuil(img_seuil, 60)
cv2.imshow('Rice', img_seuil)
# cv2.waitKey(0)

# Ouverture par reconstruction va nous permettre de degager les trop petites zone blanches et reformer un peu les grains
img_seuil = morpho.ouverture_reconstruction(img_seuil, strel.build('carre', 2), strel.build('carre', 1))
cv2.imshow('Ouverture recontruction', img_seuil)
# cv2.waitKey(0)
s2 = numpy.copy(img_seuil)

# Construction d une image ou seuls les bords sont a 255 (blanc)
m = numpy.zeros(img.shape, img.dtype)
m[0, :] = 255  # ligne haut
m[:, 0] = 255  # colonne gauche
m[-1, :] = 255  # ligne bas
m[:, -1] = 255  # colonne droite
# cv2.imshow('Bord', m)
# cv2.waitKey(0)

# La reconstruction inferieur nous permet de recup tous les grains qui sont au bord
b = morpho.reconstruction_inferieure(img_seuil, m, strel.build('carre', 1))
cv2.imshow('Bords', b)
# On retire les grains qui sont au bord
img_seuil = img_seuil - b
cv2.imshow('Sans bord', img_seuil)
# cv2.waitKey(0)

# On recup les coord des grains blancs
px, py = numpy.where(img_seuil > 0)
# On fait une image noir de la taille de l'image de depart
v = numpy.zeros(img.shape, img.dtype)
ep_largeur = numpy.zeros(img.shape, img.dtype)
ep_longueur = numpy.zeros(img.shape, img.dtype)

c=0

while px.size > 0:
    x = px[0]
    y = py[0]
    v[x, y] = 255
    ungrain = morpho.reconstruction_inferieure(img_seuil, v, gamma_8)
    v[x, y] = 0
    # On retire le grain de l'image
    img_seuil = img_seuil - ungrain

    rayon = 1.0
    s2 = numpy.copy(ungrain)

    # Tant que l'image avec le grain seul contient des pixels blanc
    while numpy.max(s2) > 0:
        rayon = rayon + 0.01
        el = strel.build('disque', rayon, None)
        s2 = morpho.ouverture(ungrain, el)

    # On recup les coord des pixels blanc pour le grain tout seul
    px_ungrain, py_ungrain = numpy.where(ungrain > 0)

    # Le nombre de pixel du grain correspond a son aire
    aire = len(px_ungrain)

    # On calcul sa longueur puisqu'on connait son aire et son rayon
    longueur = 2*aire/(math.pi*rayon)

    print (c, ' ', longueur, ' ', rayon)

    # On stocke le rayon et la longueur au coord de chaque pixel appartenant au grain de riz
    ep_largeur = ep_largeur + numpy.double(ungrain / 255) * rayon
    ep_longueur = ep_longueur + numpy.double(ungrain / 255) * longueur

    # On maj les coord des pixels blancs
    px, py = numpy.where(img_seuil > 0)
    c = c+1

print (c)

# Pour print un tableau complet
# numpy.set_printoptions(threshold=numpy.nan)
# print ep_largeur

epaisseur_max = numpy.amax(ep_largeur)
# On recup le min en ignorant les 0
epaisseur_min = numpy.amin(ep_largeur[ep_largeur > 0])
print ("Epaisseur max d'un grain : ", epaisseur_max)
print ("Epaisseur min d'un grain :", epaisseur_min)

# On met les pixels entre 100 et 255 au lieu de entre epaisseur_min et epaisseur_max
ep_largeur[ep_largeur > 0] = (ep_largeur[ep_largeur > 0] - epaisseur_min) / (epaisseur_max - epaisseur_min) * (255 - 100) + 100
cv2.imshow('Ep largeur', numpy.uint8(ep_largeur))

ep_largeur_couleur = cv2.applyColorMap(numpy.uint8(ep_largeur), cv2.COLORMAP_JET)
cv2.imshow('Ep largeur Couleur', ep_largeur_couleur)



longueur_max = numpy.amax(ep_longueur)
longueur_min = numpy.amin(ep_longueur[ep_longueur > 0])
print ("Longueur max d'un grain : ", longueur_max)
print ("Longueur min d'un grain : ", longueur_min)

# On met les pixels entre 100 et 255 au lieu de entre epaisseur_min et epaisseur_max
ep_longueur[ep_longueur > 0] = (ep_longueur[ep_longueur > 0] - longueur_min) / (longueur_max - longueur_min) * (255 - 100) + 100
cv2.imshow('Ep longueur', numpy.uint8(ep_longueur))

ep_longueur_couleur = cv2.applyColorMap(numpy.uint8(ep_longueur), cv2.COLORMAP_JET)
cv2.imshow('Ep longueur Couleur', ep_longueur_couleur)
cv2.waitKey(0)