import cv2
import numpy
from common import morpho, strel, utils

im = cv2.imread('./Images/route.png', cv2.IMREAD_GRAYSCALE)
M_bitume = cv2.imread('./Images/route_bitume.png', cv2.IMREAD_GRAYSCALE) #Marqueur 1
M_foret = cv2.imread('./Images/route_foret.png', cv2.IMREAD_GRAYSCALE) #Marqueur 2

R = numpy.zeros(im.shape, im.dtype)

Lx_bitume, Ly_bitume = numpy.where(M_bitume > 0)  # Coord ou le bitume est present
Lx_foret, Ly_foret = numpy.where(M_foret > 0)  # Coord ou la foret est presente

size = im.shape
hauteur_im = size[0]
largeur_im = size[1]

# On commence par recup les contours
im = morpho.gradient(im, strel.build('carre', 1))
# cv2.imshow("Im", im)
# cv2.waitKey(0)

list_position = []
# On stocke dans une liste les pair (x,y) pour le bitume puis la foret
for i in range(0, len(Lx_bitume)):
    list_position.append((Lx_bitume[i], Ly_bitume[i]))
for i in range(0, len(Lx_foret)):
    list_position.append((Lx_foret[i], Ly_foret[i]))

list_intensite = []
# Pour chaque pair (x,y), on recup le niveau de gris du gradient
for point in list_position:
    list_intensite.append(im[point])

# Tous les pixel representant le bitume sont a 1 et tous ceux representant la foret sont a 2
R[M_bitume > 0] = 1
R[M_foret > 0] = 2


# On traire chaque pair (x, y) jusqu'a que chaque pixel soit assigne a bitume ou foret
while len(list_position) > 0:

    # Retourne l'indice d'un minimum (on va traiter tout les pixels noir d'abord, les pixel plus grands etant les delimitations du gradient
    minim = numpy.argmin(list_intensite)

    # On recup les coord correspondant a l'indice
    coord_min = list_position[minim]

    print ("Traitement de :", coord_min)

    # Puis on le degage des listes puisqu'on va le traiter
    del list_position[minim]
    del list_intensite[minim]

    # On traite les pixels voisin tout autour de coord_min
    for i in range(-1, 2):  # 2 non compris dans le range
        for j in range(-1, 2):
            voisinx = coord_min[0] + i
            voisiny = coord_min[1] + j
            if voisinx >= 0 and voisiny >= 0 and voisinx < hauteur_im and voisiny < largeur_im:  # Secu pour pas sortir de l'image
                # Si voisin ne fait parti ni de bitume (=1) ni de foret (=2)
                if R[voisinx, voisiny] == 0:
                    # Alors maintenant il fait parti de bitume ou foret suivant les coord traite
                    R[voisinx, voisiny] = R[coord_min]
                    # Et on l'ajoute a la liste de ceux a traiter
                    list_position.append((voisinx, voisiny))
                    list_intensite.append(im[voisinx, voisiny])

# # On peut remplacer la bouble while par :
# R = morpho.ligne_des_eaux(im, R, strel.build_as_list('carre',1, None))

# On fait un gradient pour delimiter le bitume de la foret
g = morpho.gradient(R, strel.build('carre', 1))
# On seuil pour que tous soit visible puisque les pixels sont egal a 1 ou 2
g = utils.seuil(g, 1)
# cv2.imshow("Gradient seuil", g)

imc = cv2.imread('./Images/route.png')
# On met en rouge les pixel qui correspondent a la delimitation
imc[g>0] = [0, 0, 255]

cv2.imshow("Resultat", imc)

cv2.waitKey(0)