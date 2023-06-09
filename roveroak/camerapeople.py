import cv2
import numpy as np

from depthai_sdk import OakCamera
from depthai import ImgDetections, SpatialImgDetection
from depthai_sdk.classes import Detections, DetectionPacket

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

def decode(nn_data: ImgDetections):
    dets = Detections(nn_data)

    layer = nn_data.getFirstLayerFp16()
    results = np.array(layer).reshape((1, 1, -1, 7))

    for result in results[0][0]:
        if result[2] > 0.5:
            dets.add(result[1], result[2], result[3:])

    return dets

def cb(packet: DetectionPacket):
    frame = packet.visualizer.draw(packet.frame)
    cv2.imshow("frame", frame)
    for detection in packet.detections:
        img: SpatialImgDetection = detection.img_detection
        print(labels[img.label])

with OakCamera() as oak:
    color = oak.create_camera('color', resolution='1080p', encode='h265', fps=20)

    nn = oak.create_nn('mobilenet-ssd', color, nn_type='mobilenet', spatial=True, tracker=True)  # spatial flag indicates that we want to get spatial data

    nn.config_nn(conf_threshold=0.5)

    oak.visualize(nn, callback = cb)  # Display encoded output
    oak.start(blocking=True)