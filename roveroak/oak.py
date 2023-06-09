import depthai as dai

pipe = dai.Pipeline()

# Central camera setup
cam = pipe.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setFps(20)
cam.setPreviewSize(300, 300)
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Image manip setup
manip = pipe.create(dai.node.ImageManip)
manip.initialConfig.setResize(1440, 720)
manip.initialConfig.setFrameType(dai.ImgFrame.Type.YUV400p)
manip.setMaxOutputFrameSize(3500000)

# Encoder setup
encoder = pipe.create(dai.node.VideoEncoder)
encoder.setDefaultProfilePreset(20, dai.VideoEncoderProperties.Profile.H264_BASELINE)
encoder.setBitrate(1000)

# Neural Network setup
nn = pipe.create(dai.node.NeuralNetwork)
nn.setBlobPath('./roveroak/mobilenet-ssd/mobilenet-ssd.blob')
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Links
videoOut = pipe.create(dai.node.XLinkOut)
nnOut = pipe.create(dai.node.XLinkOut)
videoOut.setStreamName('video')
nnOut.setStreamName('nn')

# Linking
cam.video.link(manip.inputImage)
manip.out.link(encoder.input)
encoder.bitstream.link(videoOut.input)

cam.preview.link(nn.input)
nn.out.link(nnOut.input)


async def main():
    import websockets.server
    from base64 import b64encode
    
    async def handle(ws):
        print(ws)

    async def broadcast(server, payload: str):
        connections = list(server.websockets)

        for i in range(len(server.websockets)):
            try:
                await connections[i].send(payload)
            except IndexError:
                pass

    server = await websockets.server.serve(handle, '0.0.0.0', 8000)

    with dai.Device(pipe) as device:
        print(device.getChipTemperature().average)
        
        videoQ = device.getOutputQueue(name = 'video', maxSize = 4, blocking = False)
        nnQ = device.getOutputQueue(name = 'nn', maxSize = 4, blocking = False)

        while True:
            if server.websockets:
                encodedPacket = videoQ.get()
                encodedFrame = encodedPacket.getData().tobytes()
                
                frame_str = b64encode(encodedFrame).decode('utf-8')
                print(frame_str, end = '\n\n')
                await broadcast(server, frame_str)
            await asyncio.sleep(0.01)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
