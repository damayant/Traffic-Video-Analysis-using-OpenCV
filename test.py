import cv2 
import numpy as np 
image = cv2.imread('../Dataset/pikachu.png')
row = image[300:400,300:400,:]
pixel = row[0]
#print row 
print np.shape(row)
print row[10,10,:]
#cv2.imshow("pikachu",image)
cv2.waitKey(0)