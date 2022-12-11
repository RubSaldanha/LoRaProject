import cv2
import numpy as np

img = np.zeros((100,100,3),dtype=np.uint8)
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        img[j,i]=[j, i, (i+j) * 0.3]

cv2.imshow('a',img)
cv2.waitKey(0)
cv2.imwrite("testimage.jpg",img)
cv2.destroyAllWindows()
