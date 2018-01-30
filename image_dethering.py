#IMAGE DITHERING BASED ON Floyd-Steinberg METHOD and Stucki method
#author : bharath kotari
#date :18-1-2018


import cv2
import numpy as np


def hist_eq(im):
	clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
	cl1 = clahe.apply(im)
	return cl1
def set_pixel(im,x,y,new):
	im[x,y]=new

def stucki(im):   # stucki algorithm for image dithering
	w8= 8/42.0;
	w7=7/42.0;
	w5=5/42.0;
	w4= 4/42.0;
	w2=2/42.0;
	w1=1/42.0;
	width,height=im.shape
	for y in range(0,height-2):
		for x in range(0,width-2):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255	
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y, im[x+1,y] + w7 * quant_err);
			set_pixel(im,x+2,y, im[x+2,y]+ w5 * quant_err);
			set_pixel(im,x-2,y+1, im[x-2,y+1] + w2 * quant_err);
			set_pixel(im,x-1,y+1, im[x-1,y+1] + w4 * quant_err);
			set_pixel(im,x,y+1, im[x,y+1] + w8 * quant_err);
			set_pixel(im,x+1,y+1, im[x+1,y+1] + w4 * quant_err);
			set_pixel(im,x+2,y+1, im[x+2,y+1] + w2 * quant_err);
			set_pixel(im,x-2,y+2, im[x-2,y+2] + w1 * quant_err);
			set_pixel(im,x-1,y+2, im[x-1,y+2] + w2 * quant_err);
			set_pixel(im,x,y+2, im[x,y+2] + w4 * quant_err);
			set_pixel(im,x+1,y+2, im[x+1,y+2] + w2 * quant_err);
			set_pixel(im,x+2,y+2, im[x+2,y+2]+ w1 * quant_err);
	return im


def quantize(im):  # Floyd-Steinberg METHOD of image dithering
	for y in range(0,height-1):
		for x in range(1,width-1):
			old_pixel=im[x,y]
			if old_pixel<127:
				new_pixel=0
			else:
				new_pixel=255
			set_pixel(im,x,y,new_pixel)
			quant_err=old_pixel-new_pixel
			set_pixel(im,x+1,y,im[x+1,y]+quant_err*w1)
			set_pixel(im,x-1,y+1, im[x-1,y+1] +  quant_err*w2 )
			set_pixel(im,x,y+1, im[x,y+1] +  quant_err * w3 )
			set_pixel(im,x+1,y+1, im[x+1,y+1] +  quant_err * w4 )


	return im

img=cv2.imread("/home/user/Downloads/blender_images/barak.jpg")
#img = cv2.resize(img, (300,500), interpolation = cv2.INTER_AREA)

#res = cv2.resize(gray,(84 , 48), interpolation = cv2.INTER_AREA)
img2=img.copy()
width,height,z=img.shape
print img.shape
w1=7/16.0
#print w1
w2=3/16.0
w3=5/16.0
w4=1/16.0

gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blue=img[:,:,0]  #taking the blue channel
blue=stucki(blue)   #sending it to stucki algorithm
blue=hist_eq(blue)   #histogram equalising the result  same applies for remaining channels
green=img[:,:,1]
green=stucki(green)
green=hist_eq(green)
red=img[:,:,2]
red=stucki(red)
red=hist_eq(red)
image = cv2.merge((blue, green, red))  #merging the 3 color channels
cv2.imshow('merged_rgb',image)
gray1=hist_eq(gray)
gray1= stucki(gray1)
gray2= stucki(gray)		
cv2.imshow('original_gray',gray2)
cv2.imshow('histogram eqlised gray ',gray1)
cv2.imshow('original',img2)
cv2.waitKey(0)
