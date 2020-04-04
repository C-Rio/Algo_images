import cv2
import numpy as np

def seuil(img, seuil):
    img[img < seuil] = 0
    img[img >= seuil] = 255
    return img

def afficher(im, titre):
    cv2.imshow(titre, im)
    cv2.waitKey(0)


# La fonction de callback de la souris
# Le premier parametre decrit l'evenement de la souris qui a appele la fonction, les deux suivants donnent les coordonnes ou cet evenement a eu lieu, et le quatrieme decrit l'etat de la souris lors de l'evenement (bouton appuye, relache, etc...)
# Ces parametres sont toujours obligatoires pour cette fonction
# Le cinquieme parametre est personnalisable selon les cas
# Ici, c'est une liste avec en premier, l'image que l'on affiche et dont on va changer des couleurs de pixel
# Ensuite, trois valeurs pour specifier de quelle couleur on souhaite colorier les pixels
# Le dernier parametre est une liste de retour qui stockera les coordonnees des pixels cliques
def click_and_keep(event, x, y, flags, params):
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_MOUSEMOVE and (flags == cv2.EVENT_FLAG_LBUTTON or flags == 33): #flags ==  cv2.EVENT_FLAG_LBUTTON
    #if flags == cv2.EVENT_FLAG_LBUTTON:
        params[0][y - 1:y + 1, x - 1:x + 1] =  params[1] #On met le pixel clique a la couleur souhaitee
        cv2.imshow("Image Selection", params[0])
        params[2].append((y,x))



#Fonction permettant d'afficher une image et de recuperer les coordonnees des points cliques par l'utilisateur
def afficher_et_cliquer_image(image, color):
    marqueur = []
    im = np.copy(image)
    print ('Cliquez sur l image pour selectionner des points')
    #Creer une fenete pour obtenir les marqueurs de facon interactive
    cv2.namedWindow("Image Selection")
    #On lie cette fenetre a la fonction clickandkeep, qui sera appelee a chaque evenement de la souris
    params = [im, color, marqueur]
    cv2.setMouseCallback("Image Selection", click_and_keep, params)
    #On sort quand l'utilisateur appuie sur une touche
    cv2.imshow("Image Selection", im)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()

    return marqueur