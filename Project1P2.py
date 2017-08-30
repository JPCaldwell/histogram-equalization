####################################
#CSE473 Project 1 Problem 2
#Author: Jeremy Caldwell (jcaldwel)
####################################

import numpy as np
import cv2

#read in image
img = cv2.imread('C:\Users\Jeremy\Homework\CSE473\Python\stallman_grey.jpg', 0)
img2 = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)

#create empty histograms
hist = np.zeros(256,dtype=np.uint32)
hist2 = np.zeros(256,dtype=np.uint32)
cumHist = np.zeros(256,dtype=np.uint32)

#populate histogram for original image
for pix in np.nditer(img):
    hist[pix] += 1

#populate cumulative histogram for original image
prevSum = 0
cumHist.itemset(0,hist.item(0))
for val in range(1,256):
    cumHist[val] = cumHist.item(val-1) + hist.item(val)

#create empty dictionary to be used as lookup table
hist_memo = {}

xval = img.shape[0]
yval = img.shape[1]

#populate lookup table for memoization
for p in range(0,256):
    currItem = cumHist[p]
    temp = int(round(255.0/(xval*yval)*currItem)) #currItem/(xval * yval) calculates the values for the CDF using the cumulative histogram (xval* yval is the total number of pixels)
    hist_memo[p] = temp                           #it calculates the percentage of intensity values equal to or less than the current value
                                                  #this is where the equalized intensities are calculated by multiplying the CDF value by the total gray levels (256, starting at 0)
												  
#find transformed intensities and add them to new image
for row in range(0,xval-1):
    for col in range(0,yval-1):
        currVal = img.item(row,col)
        img2.itemset((row,col), hist_memo[currVal])

#calculate histogram for new transformed image
for pix in np.nditer(img2):
    hist2[pix] += 1

#write equalized image to disk
cv2.imwrite('eq.jpg',img2)
