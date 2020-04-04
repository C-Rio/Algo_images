import cv2
import numpy as np



#Fonction de rotation d'une image
#Prend en parametre une image, et un angle en degre
#Merci : http://stackoverflow.com/questions/9041681/opencv-python-rotate-image-by-x-degrees-around-specific-point
def rotation(image, angle_degre):
    if(len(image.shape) == 2):
        (oldY,oldX) = image.shape #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    else:
        (oldY,oldX, t) = image.shape #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=angle_degre, scale=1.0) #rotate about center of image.

    #include this if you want to prevent corners being cut off
    r = np.deg2rad(angle_degre)
    newX,newY = (abs(np.sin(r)*oldY) + abs(np.cos(r)*oldX),abs(np.sin(r)*oldX) + abs(np.cos(r)*oldY))

    #the warpAffine function call, below, basically works like this:
    # 1. apply the M transformation on each pixel of the original image
    # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

    #So I will find the translation that moves the result to the center of that region.
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx #third column of matrix holds translation, which takes effect after rotation.
    M[1,2] += ty

    rotatedImg = cv2.warpAffine(image, M, dsize=(int(newX),int(newY)))
    return rotatedImg