from flask import Flask, render_template, Response
from camera_pi import Camera
from pololu_drv8835_rpi import motors
import time
import thread

motors.setSpeeds(0, 0)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/forward')
def forward():
    speed = 360
    try:
        print("forward speed: " + str(speed))
        speed += 1
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed)
        time.sleep(0.005)
    finally:
        motors.setSpeeds(0, 0)
    
    return ('OK')

@app.route('/left')
def left():
    speed = 360
    try:
#        while speed < 480:
        print("left speed: " + str(speed))
        speed += 1
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed / 2)
        time.sleep(0.005)
    finally:
        motors.setSpeeds(0, 0)

    return ('OK')

@app.route('/right')
def right():
    speed = 360
    try:
        print("right speed: " + str(speed))
        speed += 1
        motors.motor1.setSpeed(speed / 2)
        motors.motor2.setSpeed(speed)
        time.sleep(0.005)
    finally:
        motors.setSpeeds(0, 0)

    return ('OK')

@app.route('/backward')
def backward():
    speed = 360
    try:
        print("back speed: " + str(speed))
        speed -= 1
        motors.motor1.setSpeed(speed / 2)
        motors.motor2.setSpeed(speed / 2)
        time.sleep(0.005)
    finally:
        motors.setSpeeds(0, 0)
        
    return ('OK')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    thread.start_new_thread( video_feed())
