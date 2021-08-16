import warnings
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import plot, draw, show
from pandas import DataFrame, Series
import pims
import trackpy as tp
import cv2
import glob
import os
import re
import time

#Copied from stackexchange to sort the files read by glob.glob()  
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

if __name__ == "__main__":

    
    start_time = time.time()
    print("Starting the movie making programm")

    warnings.simplefilter("ignore", RuntimeWarning)

    mpl.rc('figure',  figsize=(10, 5))
    mpl.rc('image', cmap='gray')

    frames = pims.open('/home/sagar/Documents/codes/trackpy/data/*.tif')                #Give address to files you want to make a movie of

    mm = 2000
    ps = 17
    sep = 12

    for i in range(0,len(frames)):
        f = tp.locate(frames[i], ps, invert = False, minmass = mm, separation = sep)

        plt.plot(f['x'], f['y'],'ro', markersize=1 )
        plt.imshow(frames[i]);
        figure = plt.gcf()
        figure.set_size_inches(16, 12)
        imgName = 'Fig'+str(i)+'.jpeg'
        plt.savefig(imgName)  
        plt.clf()
        plt.close()
        print("Figure %d created" % i)
         
    imgArray = []

    #The function glob.glob() doesn't take images in numerical or alphabetical order. The function numericalSort is doing that for us.
    for filename in sorted(glob.glob('*.jpeg'), key = numericalSort):
        print("Image processed = ", filename)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        imgArray.append(img)
        
    out = cv2.VideoWriter('movie2.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)        # 5 = FPS
     
    for i in range(len(imgArray)):
        out.write(imgArray[i])
    out.release()

    #Uncomment this block if need to delete all jpeg 
    for file_name in glob.glob("*.jpeg"):
           os.remove(file_name)
    print("Time taken by the program = ", time.time()-start_time)
