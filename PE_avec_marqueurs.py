import cv2
import numpy
from common import morpho, strel, utils

im = cv2.imread('./Images/route.png', cv2.IMREAD_GRAYSCALE)
imc = cv2.imread('./Images/route.png')

R = numpy.zeros(im.shape, im.dtype)

# mp1 et mp2 sont des listes
mp1 = utils.afficher_et_cliquer_image(imc, (0, 0, 255))
mp2 = utils.afficher_et_cliquer_image(imc, (255, 0, 0))

# Tous les pixel representant le bitume sont a 1 et tous ceux representant la foret sont a 2
for i, j in mp1:
    if 0 <= i < R.shape[0] and 0 <= j < R.shape[1]:
        R[i, j] = 1
for i, j in mp2:
    if 0 <= i < R.shape[0] and 0 <= j < R.shape[1]:
        R[i, j] = 2

Lx, Ly = numpy.where(R > 0)  # Coord

size = im.shape
hauteur_im = size[0]
largeur_im = size[1]

# On commence par recup les contours
im = morpho.gradient(im, strel.build('carre', 1))

list_position = []
for i in range(0, len(Lx)):
    list_position.append((Lx[i], Ly[i]))

list_intensite = []
# Pour chaque pair (x,y), on recup le niveau de gris du gradient
for point in list_position:
    list_intensite.append(im[point])

c = 0
# On traite chaque pair (x, y) jusqu'a que chaque pixel soit assigne a bitume ou foret
while len(list_position) > 0:

    minim = numpy.argmin(list_intensite)

    coord_min = list_position[minim]

    print ("Traitement de :", coord_min)

    del list_position[minim]
    del list_intensite[minim]

    for i in range(-1, 2):  # 2 non compris dans le range
        for j in range(-1, 2):
            voisinx = coord_min[0] + i
            voisiny = coord_min[1] + j
            if voisinx >= 0 and voisiny >= 0 and voisinx < hauteur_im and voisiny < largeur_im:  # Secu pour pas sortir de l'image
                if R[voisinx, voisiny] == 0:
                    R[voisinx, voisiny] = R[coord_min]
                    list_position.append((voisinx, voisiny))
                    list_intensite.append(im[voisinx, voisiny])
    c = c + 1
    if c % 1000 == 0:
        cv2.imshow("Calcul en cours", R*100)
        cv2.waitKey(1)

g = morpho.gradient(R, strel.build('carre', 1))
g = utils.seuil(g, 1)

imc[g > 0] = [0, 0, 255]

cv2.imshow("Resultat", imc)

cv2.waitKey(0)