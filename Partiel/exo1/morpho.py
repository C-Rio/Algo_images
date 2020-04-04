
import cv2
import numpy as np
import strel


# Fonction permettant de realiser l'erosion d'une image par un element structurant
def erosion(image, element_structurant):
    return cv2.erode(image, element_structurant)


# Fonction permettant de realiser la dilatation d'une image par un element structurant
def dilatation(image, element_structurant):
    return cv2.dilate(image, element_structurant)


# Fonction permettant de realiser l'ouverture d'une image par un element structurant
def ouverture(image, element_structurant):
    return dilatation(erosion(image, element_structurant), element_structurant)


# Fonction permettant de realiser la fermeture d'une image par un element structurant
def fermeture(image, element_structurant):
    return erosion(dilatation(image, element_structurant), element_structurant)


# Fonction permettant de calculer le gradient morphologique d'une image (par rapport a un element structurant)
def gradient(image, element_structurant):
    return dilatation(image, element_structurant) - erosion(image, element_structurant)


# Fonction permettant de realiser la reconstructions inferieure d'un marqueur dans une image, a l'aide d'un element structurant
def reconstruction_inferieure(image, marqueur, element_structurant):
    backup = marqueur
    dil = np.minimum(image, dilatation(backup, element_structurant))

    while( not np.array_equal(backup, dil)):
        backup = dil

        dil = np.minimum(image, dilatation(backup, element_structurant))
    return dil


# Fonction permettant de realiser l'ouverture par reconstruction d'une image
def ouverture_reconstruction(image, element_ouverture, element_reconstruction):
    op = ouverture(image, element_ouverture)
    return reconstruction_inferieure(image, op, element_reconstruction)



#Fonction permettant de realiser le h-maxima d'une image
#Prend en parametre l'image, le niveau h, et l'element structurant a utiliser pour la reconstruction
def hmaxima(image, h, element_reconstruction):
    #On rehausse toutes les valeurs de image inferieure a h, a la valeur h
    image = np.maximum(np.ones(image.shape, image.dtype)*h, image)
    #On soustrait h a image
    image2 = image - h
    #A completer
    return reconstruction_inferieure(image, image2, element_reconstruction)



#Fonction permettant de compter les composantes 8 connexes d'une image binaire
#Prend en parametre l'image binaire
def compter_morceaux(image_binaire):
    result = np.zeros(image_binaire.shape, np.uint32)
    masque = np.zeros(image_binaire.shape, image_binaire.dtype)
    compteur=0
    for i in range(0, image_binaire.shape[0]):
        for j in range(0, image_binaire.shape[1]):
            if(image_binaire[i,j] > 0):
                compteur = compteur + 1
                masque[i,j]=image_binaire[i,j]
                r = reconstruction_inferieure(image_binaire, masque, strel.build('carre', 1, None))
                image_binaire = image_binaire - r
                r = r / np.iinfo(image_binaire.dtype).max * compteur
                result = np.maximum(result, r)
                masque[i,j]=0
    return result, compteur



#Fonction permettant de realiser le seuil d'une image
#Prend en parametre l'image ainsi que la valeur du seuil
def seuil(image, seuil):
    image[image < seuil] = 0
    image[image >= seuil] = 255
    return image
