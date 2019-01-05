from flask import Flask, render_template, Response
from camera_pi import Camera
from pololu_drv8835_rpi import motors
import time
import threading

motors.setSpeeds(0, 0)

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class Cam(threading.Thread):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

class Control(threading.Thread):
    @app.route('/forward')
    def forward():
        speed = 240
	speed2 = 240
        print("forward speed: " + str(speed))
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed2)
        time.sleep(0.005)

        return ('OK')

    @app.route('/left')
    def left():
        speed = 240
	speed2 = 120
        print("left speed: " + str(speed))
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed2)
        time.sleep(0.005)

        return ('OK')

    @app.route('/right')
    def right():
        speed = 120
	speed2 = 240
        print("right speed1: " + str(speed))
	print("right speed2: " + str(speed2))
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed2)
        time.sleep(0.005)

        return ('OK')

    @app.route('/backward')
    def backward():
        speed = -120
	speed2 = -120
        print("back speed: " + str(speed))
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed2)
        time.sleep(0.005)

        return ('OK')

    @app.route('/stop')
    def stop():
        speed = 0
        motors.setSpeeds(0, 0)
        motors.motor1.setSpeed(speed)
        motors.motor2.setSpeed(speed)
        
        return('OK')
        
if __name__ == '__main__':
   
    thread1 = Control()
    thread2 = Control()
    thread3 = Control()
    thread4 = Control()
    thread5 = Control()
    thread6 = Cam()
    thread7 = Cam()
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    app.run(host='0.0.0.0', debug=True, threaded =True)
