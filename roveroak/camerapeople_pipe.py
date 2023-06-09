import depthai as dai
import cv2
from depthai import NNData
import numpy as np
from statistics import mean
from depthai_sdk.classes import Detections
from rich import inspect as ins

labels = [
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor"
]

# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = True
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Init pipeline
pipe = dai.Pipeline()

# Links
videoOut = pipe.create(dai.node.XLinkOut)
videoOut.setStreamName('video')
dispOut = pipe.create(dai.node.XLinkOut)
dispOut.setStreamName('disparity')
nnOut = pipe.create(dai.node.XLinkOut)
nnOut.setStreamName('nn')

# Central camera settings
cam = pipe.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setFps(20)
cam.setPreviewSize(300, 300)
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Stereo cameras settings
left = pipe.create(dai.node.MonoCamera)
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)
right = pipe.create(dai.node.MonoCamera)
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Depth setup
depth = pipe.create(dai.node.StereoDepth)
# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

# NeuralNetwork setup
nn = pipe.create(dai.node.NeuralNetwork)
nn.setBlobPath('./mobilenet-ssd/mobilenet-ssd.blob')
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Linking
cam.video.link(videoOut.input)
cam.preview.link(nn.input)
left.out.link(depth.left)
right.out.link(depth.right)
depth.disparity.link(dispOut.input)
nn.out.link(nnOut.input)

# Device setup
device = dai.Device(pipe)

dispQ = device.getOutputQueue(name='disparity', maxSize=4, blocking=False)
videoQ = device.getOutputQueue(name='video', maxSize=4, blocking=True)
nnQ = device.getOutputQueue(name='nn', maxSize=4, blocking=False)

def decode(nn_data: NNData):
    dets = Detections(nn_data)

    layer = nn_data.getFirstLayerFp16()
    results = np.array(layer).reshape((1, 1, -1, 7))

    for result in results[0][0]:
        if result[2] > 0.5:
            dets.add(int(result[1]), result[2], result[3:])

    return dets

while True:

    dispFrame = dispQ.get().getCvFrame()
    cv2.imshow('Disparity', dispFrame)

    nnData: NNData = nnQ.get()
    dets: Detections = decode(nnData)

    videoFrame = videoQ.get().getCvFrame()

    if len(dets.detections) > 0:
        print('In this frame there are:')
        objects = {}

        for det in dets.detections:
            det: dai.ImgDetection
            label = labels[det.label]
            if label in objects.keys():
                objects[label] += 1
            else:
                objects[label] = 1

            # Get frame dimensions (videoFrame is ndarray)
            height, width, _ = videoFrame.shape

            # Calculate absolute position for the box
            box_min = (round(det.xmin * width), round(det.ymin * height))
            box_max = (round(det.xmax * width), round(det.ymax * height))
            
            # Draw the detection box
            cv2.rectangle(videoFrame, box_min, box_max, (9,245,5), 2)
            """{"img": ..., "dets": {"person": 1, "bottle": 2}}"""
            
        
        print()

    # Show the frame
    cv2.imshow('Video', videoFrame)

    if cv2.waitKey(1) == ord('q'):
        break

device.close()