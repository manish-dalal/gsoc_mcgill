'''
Background subtraction for each frame of the image

1.Mask the central 16 pixels for every frame of the image.
2.Do steps 2 and 3 for frames 0 to 64 exluding the outlier frames (0 and 57)
2.Calculate the mean of pixel values.This is the mean background flux (bg_avg) of that frame of the image.
3.Subtract bg_avg from each pixel of that frame of image and set negative values to 0.
'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits

filepath='/home/hema/Documents/mcgill/handy/comparing/SPITZER_I2_20150000_0000_0000_1_dce.fits'
f=fits.open(filepath)
image_data=f[0].data
bgsubimg=image_data	
#Creating the mask for central 16 pixels
x=np.ndarray ( shape=(64,32,32), dtype=bool)
xmask=np.ma.make_mask(x,copy=True, shrink=True, dtype=np.bool)
xmask[:,:,:]= False
xmask[:,14:18,14:18]=True
masked= np.ma.masked_array(image_data, mask=xmask)
n=0
#Background subtraction for each frame
while(n<64):
	#1st frame and 58th frame are outliers
	if(n==0 or n==57):
		n+=1
		continue
	#Excludes NAN values in the calculations
	#bg_avg stores the average flux of the background
	bg_avg=np.median(masked[n,:,:])
	#Subtract the mean 
	bgsubimg[n]= bgsubimg[n,:,:] - bg_avg
	#Setting negative values to 0
	bgsubimg[n]= bgsubimg[n].clip(min =0)
	plt.clf()
	plt.imshow(bgsubimg[n],interpolation='none',cmap='gray')
	plt.colorbar()
	n+=1
	#plt.savefig(str(n)) #To save the img
	#plt.colorbar()	
	#plt.show()
plt.show()
f.close()
