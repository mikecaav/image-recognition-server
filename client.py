# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://ec2-44-202-146-55.compute-1.amazonaws.com:5555")

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
print(f"Host name: {rpiName}")

vs = VideoStream(src=0, resolution=(320, 240)).start()
time.sleep(2.0)
print("Video device initialized")

while True:
    frame = vs.read()
    sender.send_image(rpiName, frame)
    