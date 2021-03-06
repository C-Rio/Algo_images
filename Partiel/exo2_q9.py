import cv2
import numpy
from common import morpho, strel, utils

def rotation(image, angle_degre):
    if(len(image.shape) == 2):
        (oldY,oldX) = image.shape #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    else:
        (oldY,oldX, t) = image.shape #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=angle_degre, scale=1.0) #rotate about center of image.

    #include this if you want to prevent corners being cut off
    r = numpy.deg2rad(angle_degre)
    newX,newY = (abs(numpy.sin(r)*oldY) + abs(numpy.cos(r)*oldX),abs(numpy.sin(r)*oldX) + abs(numpy.cos(r)*oldY))

    #the warpAffine function call, below, basically works like this:
    # 1. apply the M transformation on each pixel of the original image
    # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

    #So I will find the translation that moves the result to the center of that region.
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx #third column of matrix holds translation, which takes effect after rotation.
    M[1,2] += ty

    rotatedImg = cv2.warpAffine(image, M, dsize=(int(newX),int(newY)))
    return rotatedImg

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
img = cv2.imread('./exo2/feuille2.png', cv2.IMREAD_COLOR)
cv2.imshow('img', img)

el = strel.build('disque', 4)

# image avec seulement le canal 1
img_c1 = img[:, :, 1]

#On fait une fermeture pour recuperer le fond
ferm = morpho.fermeture(img_c1, el)

#On retire le fond de l'image
img_sans_fond = ferm - img_c1

# On cherche le seuil optimal
seuil_opti = seuil_otsu(img_sans_fond)

#On applique un seuil pour faire ressortir le texte
img_seuil = utils.seuil(img_sans_fond, seuil_opti)

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
ligne_princ = morpho.ouverture(img_seuil, el)

# Images sans les lignes principales
img_sans_lignes_prin = img_seuil - ligne_princ

el = strel.build('ligne', 40, -90)
max = numpy.sum(morpho.ouverture(img_sans_lignes_prin, el))
angle2 = -90
for a in range (-90, 90, 1):
    el = strel.build('ligne', 40, a)
    g = morpho.ouverture(img_sans_lignes_prin, el)
    if (numpy.sum(g) > max) :
        max = numpy.sum(g)
        angle2 = a

print "Angle2 :", angle2

# lignes secondaire
el = strel.build('ligne', 10, angle2)
ligne_sec = morpho.ouverture(img_sans_lignes_prin, el)

# Images sans les lignes principales
img_sans_lignes = img_sans_lignes_prin - ligne_sec

el = strel.build('diamant', 1)
el2 = strel.build('carre', 2)
ims_sans_lignes_sans_bruit = morpho.ouverture_reconstruction(img_sans_lignes,el,el2)

el = strel.build('carre', 4)
img_taches = morpho.dilatation(ims_sans_lignes_sans_bruit, el)

el = strel.build('carre', 1)
img_entour = morpho.gradient(img_taches, el)

img[img_entour>0] = [0, 0, 255]

img_rot = rotation(img, -angle)
cv2.imshow('img_rot', img_rot)

# Image de base
img2 = cv2.imread('./exo2/feuille3.png', cv2.IMREAD_COLOR)
cv2.imshow('img2', img2)

el = strel.build('disque', 4)

# image avec seulement le canal 1
img2_c1 = img2[:, :, 1]

#On fait une fermeture pour recuperer le fond
ferm2 = morpho.fermeture(img2_c1, el)

#On retire le fond de l'image
img2_sans_fond = ferm2 - img2_c1

# On cherche le seuil optimal
seuil_opti = seuil_otsu(img2_sans_fond)

#On applique un seuil pour faire ressortir le texte
img2_seuil = utils.seuil(img2_sans_fond, seuil_opti)

el = strel.build('ligne', 40, -90)
max = numpy.sum(morpho.ouverture(img2_seuil, el))
angle = -90
for a in range (-90, 90, 1):
    el = strel.build('ligne', 40, a)
    g = morpho.ouverture(img2_seuil, el)
    if (numpy.sum(g) > max) :
        max = numpy.sum(g)
        angle = a

print "Angle :", angle

# lignes principales
el = strel.build('ligne', 10, angle)
ligne_princ = morpho.ouverture(img2_seuil, el)

# Images sans les lignes principales
img2_sans_lignes_prin = img2_seuil - ligne_princ

el = strel.build('ligne', 40, -90)
max = numpy.sum(morpho.ouverture(img2_sans_lignes_prin, el))
angle2 = -90
for a in range (-90, 90, 1):
    el = strel.build('ligne', 40, a)
    g = morpho.ouverture(img2_sans_lignes_prin, el)
    if (numpy.sum(g) > max) :
        max = numpy.sum(g)
        angle2 = a

print "Angle2 :", angle2

# lignes secondaire
el = strel.build('ligne', 10, angle2)
ligne_sec = morpho.ouverture(img2_sans_lignes_prin, el)

# Images sans les lignes principales
img2_sans_lignes = img2_sans_lignes_prin - ligne_sec

el = strel.build('diamant', 1)
el2 = strel.build('carre', 2)
ims2_sans_lignes_sans_bruit = morpho.ouverture_reconstruction(img2_sans_lignes,el,el2)

el = strel.build('carre', 4)
img2_taches = morpho.dilatation(ims2_sans_lignes_sans_bruit, el)


el = strel.build('carre', 1)
img2_entour = morpho.gradient(img2_taches, el)


img2[img2_entour>0] = [0, 0, 255]


img2_rot = rotation(img2, -angle)
cv2.imshow('img_rot2', img2_rot)

cv2.waitKey(0)