# Object-Tracking-and-Counting-in-a-Video
Project from scratch to track and count the number of objects moving in a scene presented in a video. This is based on Image processing and traditional computer vision techniques.
Two different methods are implemented.
Technologies Used: Python, OpenCV, Density based Clustering, Convolutions, Numpy, Matplotlib.

# Method 1:
Using Density based clustering to count moving objects in a trafiic based video.
* We extract the background first by taking a weighted aaverage of all the frames in the video based on the temporal weightage.
* We subtract the background and Extract the Frames where we only have objects in a brighter view.
* Now, We need to perform Dilation and Erosion on the frames which removes the noise
* Peform Clustering on each frame in the Frames, such that each cluster will be a Object in the Final output.
* The Number of Objcts in each frame changes as pixels of each object is encoded as a Cluster.
![image](https://user-images.githubusercontent.com/72879620/116304784-d9741e00-a79a-11eb-8019-d944248bf963.png)

# Method 2:
Using convolutions to count moving objects.
