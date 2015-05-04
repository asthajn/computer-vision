import os
os.chdir("/media/astha/Astha/CVPR/Assignments/A-2/")

import cv2
import cv2.cv as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
from copy import copy,deepcopy

image1 = cv2.imread("labPhoto.JPG" , cv2.CV_LOAD_IMAGE_GRAYSCALE) # load the grayscale image

def equalize(im):	
	breadth=im.shape[1]
	length=im.shape[0]
	
	print "no. of rows is , ", length
	print "no.of columns is , ", breadth
	
	cdf_arr= np.zeros([256,4])						#Array to store the frequency, cummulative frequency and scaled values for each pixel
	histo=np.zeros([length*breadth])
	
	for n in range(0,256):
		cdf_arr[n,0]=n
	
	min=1
	p=0
	for i in range(0,length):
		for j in range(0,breadth):
			histo[p]=im[i,j]
			p=p+1
			cdf_arr[(im[i,j]),1] = cdf_arr[(im[i,j]),1]+1
			if(cdf_arr[(im[i,j]),1] < min):
				min = cdf_arr[(im[i,j]),1]			#Storing the minimum frequency value
	print "min is " , min
	p=0
	
	for q in range(1,256):
		cdf_arr[q,2]=cdf_arr[q,1] + cdf_arr[q-1,2]
		if(cdf_arr[q,1]>0):
			cdf_arr[q,3]= (255*(cdf_arr[q,2]-min))/((length*breadth)-min)		#calculating the scaled value for each pixel
			
	for i in range(0,length):
	        for j in range(0,breadth):
			im[i,j]=cdf_arr[im[i,j],3]
			histo[p]=im[i,j]
			p=p+1
	
	os.chdir("/media/astha/Astha/CVPR/Assignments/A-2/")
	return im
	
image = equalize(image1)
cv2.imwrite('lab-equalize.JPG',image)

image = cv2.imread("lab-equalize.JPG" , cv2.CV_LOAD_IMAGE_GRAYSCALE) 		# load the grayscale image

breadth=image.shape[1]
length=image.shape[0]

print "no. of rows is , ", length
print "no.of columns is , ", breadth

lamb= np.zeros([((length-1)*(breadth-1))/49,3])

Ix=np.zeros(500)
Iy=np.zeros(500)

m=0
a=0
b=0
c=0
d=0
x=0
temp=0
tr=0
det=0

for i in range(7,length-8,7):
	for j in range(7,breadth-8,7):
		for p in range(-6,7):
			for q in range(-6,7):
				Ix[m]=int(image[i+p,j+q])-int(image[i+p,j+q+1])
				Iy[m]=int(image[i+p,j+q])-int(image[i+p+1,j+q])
				a=Ix[m]**2 +a
				b=b+Iy[m]**2
				c=(Ix[m] * Iy[m]) + c
				m=m+1
		m=0
		d=a*b
		lamb[x,0]=i
		lamb[x,1]=j
		tr=a+b
		det=d-(c**2)
		a=0
		b=0
		c=0
		d=0
		lamb[x,2]=(tr-((tr)**2 - 4*det)**(0.5))/2
		temp1=(tr+((tr)**2 - 4*det)**(0.5))/2
		if(temp1<lamb[x,2]):                            #Checking for the smaller eigen value
                        lamb[x,2]=temp1
		if(lamb[x,2] > lamb[x-1,2]):			#Sorting the eigen values
			temp=copy(lamb)
        		for w in range(0,x):
                		if (lamb[x,2]>lamb[w,2]):
                        		lamb[w,0]=lamb[x,0]
		                        lamb[w,1]=lamb[x,1]
                		        lamb[w,2]=lamb[x,2]
			                for t in range(w+1,x+1):
                        		        lamb[t,0]=temp[t-1,0]
			                        lamb[t,1]=temp[t-1,1]
                        		        lamb[t,2]=temp[t-1,2]
		x=x+1
		a=0
		b=0
		c=0
		d=0
	print i

image2=cv2.imread("labPhoto.JPG" , cv2.CV_LOAD_IMAGE_COLOR) #Load color image

for i in range(0,200):
        top=(int(lamb[i,1])-6,int(lamb[i,0])-6)
	bottom=(int(lamb[i,1])+6,int(lamb[i,0])+6)
        radius=2
        thickness=2
        cv2.rectangle(image2,top,bottom,(0,0,255,0),thickness)
        print lamb[i,0] , lamb[i,1] , lamb[i,2]

cv2.imwrite('final-3.JPG',image2)
