import cv2
import numpy as np

# Simple gradient
"""
img = np.zeros((100,100,3),dtype=np.uint8)
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        img[j,i]=[j, i, (i+j) * 0.3]
        """

# Complex Gradient
"""
c = 0
img = np.zeros((100,100,3),dtype=np.uint8)
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        img[j,i]=[j - i, i - j, c]
        c = (c + 10) % 255
        """

# Simple gray Block Gradient
"""
c = 0
init_gray = 100
img = np.zeros((100,100,3),dtype=np.uint8)
for i in range(img.shape[1]):
    for j in range(img.shape[0]):
        img[j,i]=[init_gray] * 3
    if i % 20 == 0:
        init_gray +=10
        """





cv2.imshow('a',img)
cv2.waitKey(0)
#cv2.imwrite("testimage.jpg",img)
cv2.destroyAllWindows()
