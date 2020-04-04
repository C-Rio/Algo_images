import cv2
import numpy
from common import morpho, strel, utils

img = cv2.imread('./Images/chien.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Chien', img)

#Reconstruction inferieur
masque_reconinf = cv2.imread('./Images/mask_inf.png', cv2.IMREAD_GRAYSCALE)
res_attendu_reconinf = cv2.imread('./Images/result_reconinf.png', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('Masque reconstruction inferieure', masque_reconinf)

el_reconinf = strel.build('disque', 5)

#Exemple dilatation conditionnelle
# dilat_M_E = morpho.dilatation(masque_reconinf, el_reconinf)
# cv2.imshow('Dilatation M+E', dilat_M_E)
# dilat_cond = morpho.dilatation_conditionnelle(img, masque_reconinf, el_reconinf)
# cv2.imshow('Dilatation Conditionnelle', dilat_cond)

res_reconinf = morpho.reconstruction_inferieure(img, masque_reconinf, el_reconinf)
cv2.imshow('Reconstruction inferieure', res_reconinf)

#On verif que le resulat obtenu est bien celui attendu
if numpy.array_equal(res_attendu_reconinf, res_reconinf):
    print 'Reconstruction inferieure ok'



#Reconstruction superieur
masque_reconsup = cv2.imread('./Images/mask_sup.png', cv2.IMREAD_GRAYSCALE)
res_attendu_reconsup = cv2.imread('./Images/result_reconsup.png', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('Masque reconstruction superieur', masque_reconsup)

el_reconsup = strel.build('disque', 5)

#Exemple erosion conditionnelle
# eros_M_E = morpho.erosion(masque_reconsup, el_reconsup)
# cv2.imshow('Erosion M+E', eros_M_E)
# eros_cond = morpho.erosion_conditionnelle(img, masque_reconsup, el_reconsup)
# cv2.imshow('Erosion Conditionnelle', eros_cond)

res_reconsup = morpho.reconstruction_superieure(img, masque_reconsup, el_reconsup)
cv2.imshow('Reconstruction superieure', res_reconsup)

if numpy.array_equal(res_attendu_reconsup, res_reconsup):
    print 'Reconstruction superieure ok'

cv2.waitKey(0)