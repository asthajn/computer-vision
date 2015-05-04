import os
#os.chdir("/media/astha/Astha/CVPR/Assignments/A-1/")

import cv2
import cv2.cv as cv
import numpy as np
import matplotlib.pyplot as plt
import sys

image1 = cv2.imread("airborne.jpg" , cv2.CV_LOAD_IMAGE_GRAYSCALE) 		# load the grayscale image
image2 = cv2.imread("haze.jpg" , cv2.CV_LOAD_IMAGE_GRAYSCALE) 			# load the grayscale image

cv2.imwrite('haze_gray.JPG',image2)						
def equalize(image):	
	breadth=image.shape[1]
	length=image.shape[0]
	
	print "no. of rows is , ", length
	print "no.of columns is , ", breadth
	
	def histogram(h):
	#################  Histogram  ####################
		plt.hist(h,bins = 256) 						# plotting the histogram
		plt.title("Image histogram")
		plt.xlabel("Value")
		plt.ylabel("Frequency")
		plt.show()
	#################################################
	
	cdf_arr= np.zeros([256,4])						#Array to store the frequency, cummulative frequency and scaled values for each pixel
	histo=np.zeros([length*breadth])
	
	for n in range(0,256):
		cdf_arr[n,0]=n
	
	min=1
	p=0
	for i in range(0,length):
		for j in range(0,breadth):
			histo[p]=image[i,j]
			p=p+1
			cdf_arr[(image[i,j]),1] = cdf_arr[(image[i,j]),1]+1
			if(cdf_arr[(image[i,j]),1] < min):
				min = cdf_arr[(image[i,j]),1]			#Storing the minimum frequency value
	histogram(histo)
	print "min is " , min
	p=0
	
	for q in range(1,256):
		cdf_arr[q,2]=cdf_arr[q,1] + cdf_arr[q-1,2]
		if(cdf_arr[q,1]>0):
			cdf_arr[q,3]= (255*(cdf_arr[q,2]-min))/((length*breadth)-min)		#calculating the scaled value for each pixel
			
	for i in range(0,length):
	        for j in range(0,breadth):
			image[i,j]=cdf_arr[image[i,j],3]
			histo[p]=image[i,j]
			p=p+1
	
	os.chdir("/media/astha/Astha/CVPR/Assignments/A-1/result")
	histogram(histo)
	return image
	
im = equalize(image1)
cv2.imwrite('air.JPG',im)

im = equalize(image2)
cv2.imwrite('haze.JPG',im)
	
