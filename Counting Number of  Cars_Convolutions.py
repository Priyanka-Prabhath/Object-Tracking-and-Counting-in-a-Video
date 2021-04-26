import cv2 as cv
import numpy as np
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

# takes the absolute difference between two numpy arrays
def ICV_difference(frame1,frame2):
    return cv.absdiff(frame1,frame2)

# Applies binary threshold to the image
# Creates a black and white image
def ICV_threashold(image):
    output = np.zeros(image.shape)
    for i in range (image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j]>=25:
                output[i,j] = 256
            else:
                output[i,j] = 0
    return output

# Reference: https://squawkfly.wordpress.com/2015/05/31/frame-differencing/
# Reference: https://sam-low.com/opencv/frame-differencing.html
def ICV_framedifferencing(cap, reference, flag):
    """
        cap - video file pointer
        reference - THe referencr frame used for differencing.
                    For using previous frame, reference frame is reinitialized after each iteration.
        flag - flag = 1: The reference frame is the first frame
               flag = 2: The reference frame is the I(t-1) frame
               flag = 3: The reference frame is the background 
    """
    i = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            
            f = cv.cvtColor(frame,cv.COLOR_RGB2GRAY)
            diff = ICV_difference(reference,f)
            cv.imwrite("5_output_NT_"+str(flag)+"/frame"+ str(i)+".jpg", diff)
            output = ICV_threashold(diff)
            cv.imwrite("5_output_"+str(flag)+"/frame"+ str(i)+".jpg", output)
            i+=1
            if flag == 2:
                reference = f
            
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

# Creating the background by taking the median of all the pixel values
# Reference: https://www.learnopencv.com/simple-background-estimation-in-videos-using-opencv-c-python/
def ICV_BackgroundGeneration(cap):

    frameIds = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
 
    # Store frames in an array
    frames = []
    for f in range(frameIds):
        cap.set(cv.CAP_PROP_POS_FRAMES, f)
        ret, frame = cap.read()
        frames.append(frame)

    # Calculate the median
    bkgrd = np.median(frames, axis=0).astype(dtype=np.uint8)   
 
    # Display median frame
    cv.imshow('Background', bkgrd)
    cv.waitKey(0)
    return bkgrd

# Applying basic convolution operation
def ICV_ObjectDetection(image):

    kernel = np.ones((175,175))
    kernel_size = 175
    height,width = image.shape
    conimage = np.zeros((image.shape))
    centre = kernel_size//2
    count = 0

    for x in range(centre + 50, width-centre,centre):
        for y in range(centre, height - centre, centre):
            
            p = 0
            
            for a in range (kernel_size):
                for b in range (kernel_size):
                    xn = x + a - centre
                    yn = y + b - centre
                    if xn>= height or yn>= width:
                        continue
                    pixel = image[xn, yn]
                    p +=pixel*kernel[a][b]
                    
                    
            if p>255:
                count+=1      
    
    return count



# Loading video file
cap = cv.VideoCapture("Dataset/DatasetC.avi")

#---------pixel by pixel frame differencing of a video----------------
# a) Reference frame as the first frame

# Taking the first frame as reference
ret, frame0 = cap.read()
reference = cv.cvtColor(frame0,cv.COLOR_RGB2GRAY)
# Applying frame differencing
ICV_framedifferencing(cap, reference, 1)

# b) Reference frame as the previous frame

# Resseting to the initial frame
cap.set(cv.CAP_PROP_POS_FRAMES, 0)

# Obtaining the initial frame
ret, frame0 = cap.read()
reference = cv.cvtColor(frame0,cv.COLOR_RGB2GRAY)
# Applying frame differencing
ICV_framedifferencing(cap, reference, 2)

#c) ---------Generating the background----------------
# Resseting to the initial frame
cap.set(cv.CAP_PROP_POS_FRAMES, 0)
background = ICV_BackgroundGeneration(cap)

#d) ---------Counting the number of objects in each frame----------------

# Resseting to the initial frame
cap.set(cv.CAP_PROP_POS_FRAMES, 0)
bkgrd = cv.cvtColor(background,cv.COLOR_RGB2GRAY)
# Frame differencing with the background
ICV_framedifferencing(cap, bkgrd, 3)

# Counting the objects in the video
path='5_output_3'
files = [ f for f in listdir(path) if isfile(join(path,f)) ]
count = []
for n in range(0, len(files)):
    image = cv.imread( join(path,files[n]))
    frame = cv.cvtColor(image,cv.COLOR_RGB2GRAY)
    objs = ICV_ObjectDetection(frame)
    count.append(objs)

fig = plt.figure(figsize=(10, 140))
plt.title('Object count')
plt.xlabel("Frame number")
plt.ylabel("Number of cars")

xs = np.arange(len(count)) 
width = 1
plt.bar(xs, count)
plt.show()