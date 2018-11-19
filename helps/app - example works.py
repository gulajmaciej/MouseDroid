import RPi.GPIO as GPIO
from flask import Flask, render_template
from flask import request
 
GPIO.setmode(GPIO.BCM)
 
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
 
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
 
 
app = Flask(__name__)
 
@app.route("/")
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
 
@app.route("/left")
def left():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH
 
    GPIO.output(12, sig)
    return "OK"
 
@app.route("/forward")
def forward():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH
 
    GPIO.output(6, sig)
    GPIO.output(13, sig)
    return "OK"
 
@app.route("/backward")
def backward():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH
 
    GPIO.output(5, sig)
    GPIO.output(12, sig)
    return "OK"
 
@app.route("/right")
def right():
    method = request.args.get('method')
    if method == 'stop':
        sig = GPIO.LOW
    else:
        sig = GPIO.HIGH
 
    GPIO.output(5, sig)
    return "OK"
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)
