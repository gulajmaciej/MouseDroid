from flask import Flask, render_template, Response
from camera_pi import Camera

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

@app.route('/json')
def json():
    return render_template('json.html')

@app.route('/forward')
def forward():
    while speed < 480:
        speed += 1
        motors.motor1.setSpeed(speed)
	motors.motor2.setSpeed(speed)
        time.sleep(0.005)

@app.route('/left')
def forward():
    while speed < 480:
        speed += 1
        motors.motor1.setSpeed(speed)
	motors.motor2.setSpeed(speed / 2)
        time.sleep(0.005)

@app.route('/backward')
def forward():
    while speed > -480:
        speed -= 1
        motors.motor1.setSpeed(speed / 2)
	motors.motor2.setSpeed(speed)
        time.sleep(0.005)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
