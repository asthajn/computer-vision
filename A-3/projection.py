import os
os.chdir("/media/astha/Astha/CVPR/Assignments/A-3")

import cv2
import cv2.cv as cv
import numpy as np
import math
import matplotlib.pyplot as plt

############################ Declaration of the 3-D shape ##################
pts = np.zeros([11, 3])
pts[0, :] = [-1, -1, -1]
pts[1, :] = [1, -1, -1]
pts[2, :] = [1, 1, -1]
pts[3, :] = [-1, 1, -1]
pts[4, :] = [-1, -1, 1]
pts[5, :] = [1, -1, 1]
pts[6, :] = [1, 1, 1]
pts[7, :] = [-1, 1, 1]
pts[8, :] = [-0.5, -0.5, -1]
pts[9, :] = [0.5, -0.5, -1]
pts[10,:] = [0, 0.5, -1]


def quatmult(p, q):
	# quaternion multiplication
	a=p[0]*q[0]-p[1]*q[1]-p[2]*q[2]-p[3]*q[3]
	b=q[0]*p[1]+q[1]*p[0]+q[2]*p[3]-q[3]*p[2]
	c=q[0]*p[2]-q[1]*p[3]+q[2]*p[0]+q[3]*p[1]
	d=q[0]*p[3]+q[1]*p[2]-q[2]*p[1]+q[3]*p[0]
	out=[a,b,c,d]
	return out
	 # output array to hold the result
	
################################### Quarternion rotation for the camera orientation ####################################
def quat2rot(q):
	a=np.array([pow(q[0],2)+pow(q[1],2)-pow(q[2],2)-pow(q[3],2) , 2*(q[1]*q[2]-q[0]*q[3]) , 2*(q[1]*q[3]+q[0]*q[2])])
	b=np.array([2*(q[1]*q[2]+q[0]*q[3]) , pow(q[0],2)+pow(q[2],2)-pow(q[1],2)-pow(q[3],2) , 2*(q[2]*q[3]-q[0]*q[1])])
	c=np.array([2*(q[1]*q[3]-q[0]*q[2]) , 2*(q[2]*q[3]+q[0]*q[1]) , pow(q[0],2)+pow(q[3],2)-pow(q[1],2)-pow(q[2],2)])
	quatmat_=np.array([a,b,c])
	quatmat1=np.matrix(quatmat_)
	return quatmat1

############################## Conjugate of a quaternion #############################
def conjugate(q):
	return [math.cos(theta/2),0,-(math.sin(theta/2)),0]

############################### Declaration of the variables #########################

i=0
u0=0
v0=0
Bu=1
Bv=1
focal=1
x=np.zeros([4,4])
quaternion=[0,0,0,-5]
q0=np.array([4])
q1=np.array([4])
u=np.zeros([4,11])
v=np.zeros([4,11])
uortho=np.zeros([4,11])
vortho=np.zeros([4,11])
camera_rotation=np.matrix(np.identity(3))

############################### Calculating the quaternions for the four frames ###############################
############################## 	the rotation matrices and the projection points ###############################
for i in range(0,4):
	theta=-(math.pi)/6						
	print "theta is : ", i*theta
	q0=[math.cos(theta/2),0,math.sin(theta/2),0]
	
	quaternion=quatmult(conjugate(q0),quatmult(quaternion,q0))	# calculating the quaternion for each frame
	theta=(i*math.pi)/6
	q0=[math.cos(theta/2),0,math.sin(theta/2),0]
	print "Quaternion is : ",quaternion
	camera_rotation=quat2rot(q0)					# calculating the rotation matrix for each frame
	if(i==0):
		camera_rotation=np.identity(3)
                quaternion=[0,0,0,-5]
	camera=[quaternion[1],quaternion[2],quaternion[3]]		# storing the translated coodinates of the camera
	################################ Perspective projection ####################################
			
	for j in range(0,11):
		sp=(np.matrix(pts[j,:]-camera))
		iaxis=np.matrix(camera_rotation[0,:])
		jaxis=np.matrix(camera_rotation[1,:])
		kaxis=np.matrix(camera_rotation[2,:])
		u[i,j]=(focal*((sp)*np.transpose(iaxis))*Bu)/((sp)*np.transpose(kaxis)) + u0

		v[i,j]=(focal*((sp)*np.transpose(jaxis))*Bv)/((sp)*np.transpose(kaxis)) + v0
		print "U vs V is : ", u[i,j],"	",v[i,j],"\n"
		
	#############################################################################################

	###############################Orthographic projction#######################################
	for j in range(0,11):
		sp=(np.matrix(pts[j,:]-camera))
                iaxis=np.matrix(camera_rotation[0,:])
                jaxis=np.matrix(camera_rotation[1,:])
		uortho[i,j]=(sp*np.transpose(iaxis)) * Bu +u0
		vortho[i,j]=(sp*np.transpose(jaxis)) * Bv +v0
		print "U-O vs V-O is : ", uortho[i,j],"	",vortho[i,j],"\n"
	##############################################################################################		

########################################### Plotting the points #######################################
########################################### Perspective Plotting ######################################

plt.subplot(221, axisbg='y')
plt.scatter(u[0,:],v[0,:])
plt.title("Perspective Frame-1")

plt.subplot(222, axisbg='y')
plt.scatter(u[1,:],v[1,:])
plt.title("Perspective Frame-2")

plt.subplot(223, axisbg='y')
plt.scatter(u[2,:],v[2,:])
plt.title("Perspective Frame-3")

plt.subplot(224, axisbg='y')
plt.scatter(u[3,:],v[3,:])
plt.title("Perspective Frame-4")
plt.savefig("Perspective.jpg")
plt.show()

########################################### Orthographic Plotting ######################################

plt.subplot(221, axisbg='b')
plt.scatter(uortho[0,:],vortho[0,:])
plt.title("Orthographic Frame-1")

plt.subplot(222, axisbg='b')
plt.scatter(uortho[1,:],vortho[1,:])
plt.title("Orthographic Frame-2")

plt.subplot(223, axisbg='b')
plt.scatter(uortho[2,:],vortho[2,:])
plt.title("Orthographic Frame-3")

plt.subplot(224, axisbg='b')
plt.scatter(uortho[3,:],vortho[3,:])
plt.title("Orthographic Frame-4")
plt.savefig("Orthographic.jpg")

plt.show()

