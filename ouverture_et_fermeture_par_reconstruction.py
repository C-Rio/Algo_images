import cv2
import numpy
from common import morpho, strel, utils

img = cv2.imread('./Images/chien.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Chien', img)


#Ouverture par reconstruction
res_attendu_opencond = cv2.imread('./Images/result_opencond.png', cv2.IMREAD_GRAYSCALE)

el_opencond = strel.build('disque', 20)

gamma_8 = strel.build('carre', 1)

# cv2.imshow('Ouverture', morpho.ouverture(img, el_opencond))

res_opencond = morpho.ouverture_reconstruction(img, el_opencond, gamma_8)
cv2.imshow('Ouverture reconstruction', res_opencond)

if numpy.array_equal(res_attendu_opencond, res_opencond):
    print 'Ouverture reconstruction inferieure ok'



#Fermeture par reconstruction
res_attendu_closecond = cv2.imread('./Images/result_closecond.png', cv2.IMREAD_GRAYSCALE)

el_closecond = strel.build('disque', 20)

gamma_8 = strel.build('carre', 1)

res_closecond = morpho.fermeture_reconstruction(img, el_closecond, gamma_8)
cv2.imshow('Fermeture reconstruction', res_closecond)

if numpy.array_equal(res_attendu_closecond, res_closecond):
    print 'Fermeture reconstruction inferieure ok'
cv2.waitKey(0)