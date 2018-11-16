def start():
    while speed < 480:
        speed += 1
        print(speed)
        #motors.motor1.setSpeed(speed)
        time.sleep(0.005)

def stop():
    while speed > 0:
        speed += -1
        print (speed)
        #motors.motor1.setSpeed(speed)
        time.sleep(0.005)