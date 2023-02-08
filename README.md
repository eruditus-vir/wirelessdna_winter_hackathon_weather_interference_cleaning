# Wireless DNA hackathon 

data at https://filesender.funet.fi/?s=download&token=d05d4253-ef08-439e-968f-a10ef84877a4

## Problem Statement 
Reconstruction of radar to infer rain 
Radar dataset 
What is doppler radar? Radar for weather. Circulation of wind?
radar shoot electro at specific elevation and bounce off and return to receiver.
signal reflected get back and processed into reflectivity and velocity.
Radar is at height, not reflection of things below or at the ground.

Problem: ground vs radar 
Problem: resolution, 1 km resolution, only show overall within 1 km box. 
Problem: radar errors --> normal; refraction, superrefraction, subrefraction, ducting (mountains and obstructions)

## Objective  
Digitalize radar values and locate the img pixels on real locations (lat/lng of pixels) --> because of radar errors 
Detect interferences
Delete interferences
Correct interferences 
Save data into a file in netCDF format. 

## Data and Assumptions 
Real radar dataof 5 months
saptial resolution of 1km per pixel 
sampling rate of 10 minutes --> maybe interferences doesnt change between the images 

ba, pm, va --> locations
then inside is each day with 10 min intervals

each image from each area kinda overlap with each other --> u can correlate and check for interferences. 
dry: jan, feb
wet: apri, may

last half of may for testing is the best

missing images is possible 

forecast 2 hours with the last 6 images --> but we are going to correct these images 