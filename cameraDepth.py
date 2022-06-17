from operator import length_hint
from re import S
import cv2
import depthai as dai
import numpy as np
import pwmraspberry as pwm
import sys
# import server as serv
# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)
xoutVideo.setStreamName("video")


# Properties
camRgb.setPreviewSize(640, 480)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.video.link(xoutVideo.input)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # m

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)

xout.setStreamName("disparity")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)



def resize_percent(scale_percent, src):

    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    dsize = (width, height)

    output = cv2.resize(src, dsize)
    return output


def zone_matrix(divX, frame):
    lenX = len(frame[0])  
    lenY = len(frame)
    ## totals ##
    totals = [0] * divX
    limX = int(lenX/divX)
    iterX=countX=0
    for y in range(int(lenY/2),lenY, 1):
        iterX=countX=0
        for x in range(0,lenX, 1):
            if countX==limX:    
                countX=0
                iterX+=1
            if iterX < divX:
                totals[iterX] += frame[y][x] 
            countX+=1     
    for i in range(0,len(totals),1):
        totals[i] = int(totals[i] / lenY/2)
    for i in range(1,limX,1):
        frame = cv2.rectangle(frame, ((int(lenX/divX)*(i-1)),int(lenY/2)), ((int(lenX/divX)*i),lenY), (255,255,255), 2)
    return totals   
def find_path(totals,steering): # steering è un int che va da -5 a 5
    arr = np.array(totals) 
    lenT = len(arr)
    min_val = arr.min()
    min_idxs = [idx for idx, val in enumerate(arr) if val == min_val]              
    print ("min_idxs = {0}".format(min_idxs))
    # adjust = 0
    # if steering > 0: #deve andare a destra
    #     for minArr in min_idxs:
    #         if minArr < lenT/2:
    #             adjust = minArr #trova quello più a destra
    #     steering = steering + (adjust-(lenT/2))
    #     if steering > 5:
    #         steering = 5
    #     print("Destra di: ", steering)
    # elif steering < 0:
    #     for minArr in min_idxs:
    #             if minArr > lenT/2:
    #                 adjust = minArr #trova quello più a destra
    #     steering = steering - (adjust-(lenT/2))
    #     if steering < -5:
    #         steering = -5
    #     print("Sinistra di: ", steering)
    # else:
    #     print("Dritto")
    






# Connect to device and start pipeline
device = dai.Device(pipeline) 
video = device.getOutputQueue(name="video", maxSize=4, blocking=False)
q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
kernel = np.ones((13,13),dtype="uint8")
while True:    
    inDisparity = q.get()
    frame = inDisparity.getFrame()


    # inRgb = video.get()  
    # videoFrame = inRgb.getCvFrame()
    # cv2.imshow("video", resize_percent(40,videoFrame))

    frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
    frame = resize_percent(60,frame)
    frame = cv2.erode(frame, kernel)
    frame = cv2.dilate(frame, kernel)
    ret,frame = cv2.threshold(frame, 130, 255, cv2.THRESH_TOZERO)
    totals = zone_matrix(8,frame) 
    print(totals)
    find_path(totals, 1)
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_OCEAN)
    cv2.imshow("depth frame", frame)   
    if cv2.waitKey(1) == ord('q'):
        break 