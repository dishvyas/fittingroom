#!/usr/bin/python

import cv2
import numpy as np
from scipy import ndimage


#Resize an image to a certain width
def resize(img, width,height = None):
   
    if height is not None:
        img = cv2.resize(img, (width,height), interpolation=cv2.INTER_AREA)
    else:
        r = float(width) / img.shape[1]
        dim = (width, int(img.shape[0] * r))
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow('a',img)

    return img

#Combine an image that has a transparency alpha channel
def blend_transparent(face_img, sunglasses_img):

    overlay_img = sunglasses_img[:,:,:3]
    overlay_mask = sunglasses_img[:,:,3:]
    
    background_mask = 255 - overlay_mask

    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

#Find the angle between two points
def angle_between(point_1, point_2):
    angle_1 = np.arctan2(*point_1[::-1])
    angle_2 = np.arctan2(*point_2[::-1])
    return np.rad2deg((angle_1 - angle_2) % (2 * np.pi))


#Start main program
def get2dfit(TSHIRTLOC, PERSONPIC,LS,RS,TOP,BOT):

    glasses = cv2.imread(TSHIRTLOC, -1)
    img = cv2.imread(PERSONPIC)
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # import matplotlib.pyplot as plt
    # plt.imshow(img)
    # plt.show()  
    # exit()

    ##############   Resize and rotate glasses   ##############

    #Translate facial object based on input object.

    y = TOP[1] - 350 #600 #Top 1st field
    eye_left = LS #(240,1432) #Left Shoulder
    eye_right = RS #(1619,1422) #Right Shoulder
    x=eye_left[0]
    w=eye_right[0]
    bottom = BOT[1] #2280 #Bottom 1st field
    print(y)
    # import matplotlib.pyplot as plt
    # plt.imshow(img)
    # plt.show()
    try:
        #cv2.line(img_copy, eye_left, eye_right, color=(0, 255, 255))
        degree = np.rad2deg(np.arctan2(eye_left[0] - eye_right[0], eye_left[1] - eye_right[1]))

    except:
        pass

    eye_center = (eye_left[1] + eye_right[1]) / 2

    #Sunglasses translation
    glass_trans = int(.2 * (eye_center - y))

    #Funny tanslation
    #glass_trans = int(-.3 * (eye_center - y ))

    # Mask translation
    #glass_trans = int(-.8 * (eye_center - y))

    face_width = abs(eye_left[0] - eye_right[0])

    # resize_glasses
    glasses_resize = resize(glasses, face_width,bottom-y)

    # Rotate glasses based on angle between eyes
    yG, xG, cG = glasses_resize.shape
    glasses_resize_rotated = ndimage.rotate(glasses_resize, (degree+90))
    # print(type(x), type(w))
    glass_rec_rotated = ndimage.rotate(img[y + glass_trans:y + yG + glass_trans, eye_left[0]:eye_right[0]], (degree+90))
    
    #blending with rotation
    h5, w5, s5 = glass_rec_rotated.shape

    # x X+w5
    rec_resize = img_copy[y + glass_trans:y + h5 + glass_trans, x:x+w5]
    blend_glass3 = blend_transparent(rec_resize , glasses_resize_rotated)
    img_copy[y + glass_trans:y + h5 + glass_trans, x:x+w5] = blend_glass3

    cv2.imwrite('/home/dishant/Desktop/Assignments/Hackathon/static/r2esult.jpg',img_copy)
get2dfit('/home/dishant/Desktop/Assignments/Hackathon/templates/t3.png',"/home/dishant/Desktop/Assignments/Hackathon/static/uploads/exp1.jpg",(258,1444),(1620,1424),(976,932),(904,2312)) 