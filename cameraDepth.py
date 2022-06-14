from re import S
import cv2
import depthai as dai
import numpy as np
import pwmraspberry as pwm
# import server as serv
# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Create pipeline
pipeline = dai.Pipeline()

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

# Connect to device and start pipeline
device = dai.Device(pipeline) 

# Output queue will be used to get the disparity frames from the outputs defined above
q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
kernel = np.ones((15,15),dtype="uint8")
#kernel = np.ones((6, 6), np.uint8)
inDisparity = q.get()  # blocking call, will wait until a new data has arrived
frame = inDisparity.getFrame()

############################working on###########################
def resize_percent(perc, src):
    scale_percent = 50

    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    output = cv2.resize(src, dsize)
    return output
def zone_matrix(divX,divY):
    lenX = len(frame[0])  
    lenY = len(frame)  
    totals = [[] * divX]*divY  
    iterX=iterY=i=j=0 
    for iterY in range(0,divY):
        for iterX in range(0,divX):
            for i in range(0,int(lenX), 1):
                for j in range(0,int(lenY), 1):
                    totals[iterX][iterY] += frame[int(lenY/divY)*iterY][int(lenX/divX)*iterX] #check
                    
    # mDX = int(totals[0]/count)
    # mFW = int(totals[1]/count)
    # mSX= int(totals[2]/count)
    # minVal = min(mDX,mFW,mSX)
    # print(minVal) 
    # print("SINISTRA",mSX) 
    # print("DESTRA",mDX)
    # print("FORWARD",mFW)  
    # if mFW == 0:  
    #     print("--FORWARD")
    #     pwm.traz(3,0)
    # elif mSX == minVal:
    #     print("--SINISTRA")
    #     pwm.traz(-5,0)
    #     pwm.traz(3,-5)
    # elif mDX == minVal:
    #     print("--DESTRA")
    #     pwm.traz(-5,0)
    #     pwm.traz(3,5)
    # else: 
    #     pwm.traz(3,0)
    #     print("--FORWARD")
while True:
    inDisparity = q.get() 
    frame = inDisparity.getFrame()
    frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
    frame = cv2.erode(frame, kernel)
    frame = cv2.dilate(frame, kernel)
    ret,frame = cv2.threshold(frame,180, 255, cv2.THRESH_TOZERO)
    frame = resize_percent(50,frame)
    # #funzione che calcola una matrice con le medie delle vare zone
    
    frame = cv2.applyColorMap(frame, cv2.COLORMAP_PLASMA)
    # frame = cv2.rectangle(frame, (0,0), (int(lenX/3),400), (255,255,255),3)
    # frame = cv2.rectangle(frame, (int(lenX/3),0), (int(lenX/3*2),400), (255,0,255),3)
    # frame = cv2.rectangle(frame, (int(lenX/3*2),0),(int(lenX),400) , (255,255,0),3)
    cv2.imshow("disparity", frame)
    if cv2.waitKey(1) == ord('q'):
        break 