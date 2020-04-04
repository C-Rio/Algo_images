import cv2
import numpy
from common import morpho, strel, utils


img = cv2.imread('./Images/rice.png', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('Rice', img)

gamma_8 = strel.build('carre', 1)

el = strel.build('disque', 30)
ouv = morpho.ouverture(img, el)

img_seuil = img - ouv
img_seuil = utils.seuil(img_seuil, 60)

# cv2.imshow('Rice seuil', img_seuil)
# cv2.waitKey(0)

s2=numpy.copy(img_seuil)
#Recup les coord des pixels >0
px,py = numpy.where(img_seuil>0)

#Image noir de la meme taille que rice.png
v = numpy.zeros(img.shape, img.dtype)

nb_rice=0
#On continu tant qu'il reste des pixels >0 donc des grains de riz
while px.size > 0:
    # On prend le premier pixel >0
    x = px[0]
    y = py[0]

    #On le met en full blanc
    v[x,y] = 255

    #On recup le grain complet
    ungrain = morpho.reconstruction_inferieure(img_seuil, v, strel.build('carre', 1))
    # cv2.imshow('Grain', ungrain)
    # cv2.waitKey(0)

    #On passe en noir le pixel traite
    v[x,y] = 0

    #On supprime le grain de l'image
    img_seuil = img_seuil-ungrain

    # On maj les coord des pixels >0
    px, py = numpy.where(img_seuil>0)

    nb_rice = nb_rice + 1
    # print c


print 'Nombre de grains de riz : ', nb_rice

# cv2.waitKey(0)


# Old
# masque = numpy.zeros(img.shape, img.dtype)
# count = 0
# img_copy = numpy.copy(img_seuil)
# for i in range(0, img.shape[0]):
#     for j in range(0, img.shape[1]):
#         masque[i][j] = 255
#         reconf_inf = morpho.reconstruction_inferieure(img_copy, masque, gamma_8)
#         masque[i][j] = 0
#         if(numpy.sum(reconf_inf) > 0):
#             count = count + 1
#             img_copy = img_copy - reconf_inf
#             print count
#
# print 'Nombre de grains de riz : ', count