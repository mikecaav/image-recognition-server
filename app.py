from flask import Flask, render_template, request
from flask.wrappers import Response
import imagezmq
import cv2
import socket

app = Flask(__name__)
camera = cv2.VideoCapture(0)

rpiName = socket.gethostname()
receiver = imagezmq.ImageSender(connect_to="tcp://ec2-44-202-146-55.compute-1.amazonaws.com:5555")

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/video-feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

if __name__ == "__main__":
    app.run()
