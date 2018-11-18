from __future__ import print_function
import time
from flask import Flask, render_template, Response
from camera_pi import Camera
from pololu_drv8835_rpi import motors, MAX_SPEED

app = Flask(__name__)
buttonStatus = 1

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    while buttonStatus == 1:
	test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
      [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]

    	try:
            motors.setSpeeds(0, 0)
            for s in test_forward_speeds:
            	motors.motor1.setSpeed(s)
                motors.motor2.setSpeed(s)
            	time.sleep(0.005)
    	finally:
        	motors.setSpeeds(0, 0)

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/background_process_test')
def background_process_test():
    if buttonStatus == 1:
	buttonStatus = 0
    else:
        buttonStatus = 1

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000, debug=True)
