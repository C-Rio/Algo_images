import cv2
import numpy

def erosion(img, el):
    return cv2.erode(img, el)

def dilatation(img, el):
    return cv2.dilate(img, el)

def gradient(img, el):
    return dilatation(img, el) - erosion(img, el)

def ouverture(img, el):
    return dilatation(erosion(img, el), el)

def fermeture(img, el):
    return erosion(dilatation(img, el), el)

def dilatation_conditionnelle(img, m, el):
    return numpy.minimum(img, dilatation(m, el))

def erosion_conditionnelle(img, m, el):
    return numpy.maximum(img, erosion(m, el))

def reconstruction_inferieure(img, m, el):
    prec = m
    actuel = dilatation_conditionnelle(img, prec, el)
    while not numpy.array_equal(prec, actuel):
        prec = actuel
        actuel = dilatation_conditionnelle(img, prec, el)
        # cv2.imshow('Iteration reconstruction inferieur', actuel)
        # cv2.waitKey(0)
    return actuel

def reconstruction_superieure(img, m, el):
    prec = m
    actuel = erosion_conditionnelle(img, prec, el)
    while not numpy.array_equal(prec, actuel):
        prec = actuel
        actuel = erosion_conditionnelle(img, prec, el)
        # cv2.imshow('Iteration reconstruction superieur', actuel)
        # cv2.waitKey(0)
    return actuel

def ouverture_reconstruction(im, el_op, el_r):
    op = ouverture(im, el_op)
    # cv2.imshow('Ouverture', op)
    # cv2.waitKey(0)
    return reconstruction_inferieure(im, op, el_r)

def fermeture_reconstruction(im, el_fe, el_r):
    op = fermeture(im, el_fe)
    return reconstruction_superieure(im, op, el_r)

# def reconstruction_inferieure_recursif(img, m, el):
#     img2 = dilatation_conditionnelle(img, m, el)
#     if numpy.array_equal(m, img2):
#         return img2
#     else:
#         return reconstruction_inferieure_recursif(img, img2, el)
#
# def reconstruction_superieure_recursif(img, m, el):
#     img2 = erosion_conditionnelle(img, m, el)
#     if numpy.array_equal(m, img2):
#         return img2
#     else:
#         return reconstruction_superieure_recursif(img, img2, el)

def ligne_des_eaux(img, marqueur, el):
    Lp = []
    Li = []
    el = numpy.array([[i,j] for i,j in el])
    R = marqueur
    Lp = [i for i in numpy.argwhere(R>0)]
    Li = [img[i[0], i[1]] for i in Lp]
    nb = 0
    cv2.imshow('En cours', R * 100)
    while len(Lp)!= 0:
        v = min(Li)
        idx = Li.index(v)
        i = Lp[idx]
        del Lp[idx]
        del Li[idx]
        voisin = el+i
        nb+=1
        for x,y in voisin:
            if x>=0 and y>=0 and x<R.shape[0] and y<R.shape[1] and R[x,y]==0:
                R[x,y]=R[i[0], i[1]]
                Lp.append([x,y])
                Li.append(img[x][y])
        if(nb%100==0):
            cv2.imshow('En cours', R*100)
            cv2.waitKey(1)
    return R
