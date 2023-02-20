# Wireless DNA hackathon 

data at https://filesender.funet.fi/?s=download&token=d05d4253-ef08-439e-968f-a10ef84877a4

Result: Won through using method from Vaisala

## Problem Statement 
Delete, delete and reconstruct radar interferences.

## Objective  
Digitalize radar values and locate the img pixels on real locations (lat/lng of pixels) --> because of radar errors 
Detect interferences
Delete interferences
Correct interferences 
Save data into a file in netCDF format. 

## Data and Assumptions 
Real radar data of 5 months
saptial resolution of 1km per pixel 
sampling rate of 10 minutes --> maybe interferences doesnt change between the images 

ba, pm, va --> locations
then inside is each day with 10 min intervals

each image from each area kinda overlap with each other --> u can correlate and check for interferences. 
dry: jan, feb
wet: apri, may

last half of may for testing is the best

missing images is possible 

## Digitalization and Visualization Step 
Simple reading with pillow and cropping with pillow (including the radar circle). 


## Interference Detection Step

Methods Tried 
- Line detections  
- Deep Learning
- Azimuth Radial Differential detection + Signal Professing (This worked very well )
  - https://ams.confex.com/ams/101ANNUAL/meetingapp.cgi/Paper/383907