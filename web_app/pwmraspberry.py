import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(38, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)

freq = 500
left1 = GPIO.PWM(38, freq)
left2 = GPIO.PWM(37, freq)
right1 = GPIO.PWM(12, freq)
right2 = GPIO.PWM(35, freq)


def setup_pwm():
    left1.start(0)
    left2.start(0)
    right1.start(0)
    right2.start(0)


def stop_pwm():
    left1.stop()
    left2.stop()
    right1.stop()
    right2.stop()


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def traz(velocita, sterzo):
    if sterzo < 0:
        sterzo = -sterzo
        v_dx = velocita
        v_sx = map(sterzo, 0, 5, velocita, -velocita)
    else:
        v_dx = map(sterzo, 0, 5, velocita, -velocita)
        print(v_dx)
        v_sx = velocita

    if v_dx < 0:
        v_dx = -v_dx
        v_dx = map(v_dx, 0, 5, 0, 100)
        right1.ChangeDutyCycle(0)
        right2.ChangeDutyCycle(v_dx)
    else:
        v_dx = map(v_dx, 0, 5, 0, 100)
        right1.ChangeDutyCycle(v_dx)
        right2.ChangeDutyCycle(0)

    if v_sx < 0:
        v_sx = -v_sx
        v_sx = map(v_sx, 0, 5, 0, 100)
        left1.ChangeDutyCycle(0)
        left2.ChangeDutyCycle(v_sx)
    else:
        v_sx = map(v_sx, 0, 5, 0, 100)
        left1.ChangeDutyCycle(v_sx)
        left2.ChangeDutyCycle(0)


# # # # # # # # # # # # # # # # # # MAIN # # # # # # # # # # # # # # # # # #
# setup_pwm()

# traz(5,0)
# sleep(5)

# stop_pwm()
