import cv2
import numpy as np

img=cv2.imread("artwork_picasso.png",0)
img_org=cv2.imread("result.png",0)



box1 = np.full([img.shape[0], img.shape[1]], 251, dtype=np.uint8) #10*pi*8
box2 = np.full([img.shape[0], img.shape[1]], 219, dtype=np.uint8) #10*pi*7
box3 = np.full([img.shape[0], img.shape[1]], 94, dtype=np.uint8) #10*pi*3
box4 = np.full([img.shape[0], img.shape[1]], 0, dtype=np.uint8) #10*pi*0

img1=np.full((100,100),0, dtype=np.uint8)
img_fil=np.zeros((100,100), dtype=np.uint8)
img3 = np.full((100, 100), 0, dtype=np.uint8)
img5 = np.full((100, 100), 0, dtype=np.uint8)


for i in range(img.shape[0]):
    for j in range(img.shape[1]):

        img1 = cv2.bitwise_xor(img, box1)
        if (i % 2 == 0 and j % 2 == 0):
            img_fil[i, j] = img1[i, j]

        img2 = cv2.bitwise_xor(img, box2)
        if (i % 2 == 0 and j % 2 == 1):
            img_fil[i, j] = img2[i, j]

        img3 = cv2.bitwise_xor(img, box3)
        if (i % 2 == 1 and j % 2 == 0):
            img_fil[i, j] = img3[i, j]


        img4 = cv2.bitwise_xor(img, box4)
        if (i % 2 == 1 and j % 2 == 1):
            img_fil[i, j] = img4[i, j]



cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img', img)
cv2.namedWindow('img_filtered', cv2.WINDOW_NORMAL)
cv2.imshow('img_filtered', img_fil)
cv2.waitKey(0)
