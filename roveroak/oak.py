import depthai as dai

BLOB = './roveroak/mobilenet-ssd/mobilenet-ssd.blob'

async def create_pipeline(rgbOutputSize = (832, 480), confidence = .5, extended_disparity = True, subpixel = False, lr_check = True):
    # Create pipeline
    pipeline = dai.Pipeline()

    # Camera settings
    cam = pipeline.create(dai.node.ColorCamera)
    cam.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam.setFps(20)
    cam.setPreviewSize(300, 300)
    cam.setInterleaved(False)
    cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

    monoLeft = pipeline.create(dai.node.MonoCamera)
    monoLeft.setResolution(dai.MonoCameraProperties.resolution.THE_400_P)
    monoRight = pipeline.create(dai.node.MonoCamera)
    monoRight.setResolution(dai.MonoCameraProperties.resolution.THE_400_P)

    # StereoDepth setup
    stereo = pipeline.create(dai.node.StereoDepth)
    # Setting node configs
    stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_ACCURACY)
    # Align depth map to the perspective of RGB camera, on which inference is done
    stereo.setDepthAlign(dai.CameraBoardSocket.CENTER)
    stereo.setSubpixel(subpixel)
    stereo.setLeftRightCheck(lr_check)
    stereo.setExtendedDisparity(extended_disparity)
    stereo.setOutputSize(monoLeft.getResolutionWidth(), monoLeft.getResolutionHeight())


    # SpatialNN setup
    mobilenetSpatial = pipeline.create(dai.node.MobileNetSpatialDetectionNetwork)
    mobilenetSpatial.setNumInferenceThreads(2)
    mobilenetSpatial.setBlobPath(BLOB)
    # Will ingore all detections whose confidence is below 50%
    mobilenetSpatial.setConfidenceThreshold(confidence)
    mobilenetSpatial.input.setBlocking(False)
    # How big the ROI will be (smaller value can provide a more stable reading)
    mobilenetSpatial.setBoundingBoxScaleFactor(0.5)
    # Min/Max threshold. Values out of range will be set to 0 (invalid)
    mobilenetSpatial.setDepthLowerThreshold(100)
    mobilenetSpatial.setDepthUpperThreshold(5000)


    # Resizer setup
    manip = pipeline.create(dai.node.ImageManip)
    # 480p 16:9 frames
    manip.initialConfig.setResize(rgbOutputSize[0], rgbOutputSize[1])
    # NV12 frames are supported by video encoder
    manip.initialConfig.setFrameType(dai.ImgFrame.Type.NV12)
    manip.setMaxOutputFrameSize(2000000)

    # Video Encoder setup
    videoEnc = pipeline.create(dai.node.VideoEncoder)
    videoEnc.setDefaultProfilePreset(20, dai.VideoEncoderProperties.Profile.MJPEG)
    # videoEnc.setBitrateKbps(100)

    # Links
    videoOut = pipeline.create(dai.node.XLinkOut)
    videoOut.setStreamName('video')
    nnOut = pipeline.create(dai.node.XLinkOut)
    nnOut.setStreamName('nn')

    # Linking
    cam.video.link(manip.inputImage)
    cam.preview.link(mobilenetSpatial.input)

    monoLeft.out.link(stereo.left)
    monoRight.out.link(stereo.right)
    # manip.out.link(videoEnc.input)
    # videoEnc.bitstream.link(videoOut.input)

    # Link depth from the StereoDepth node
    stereo.depth.link(mobilenetSpatial.inputDepth)