import RPi.GPIO as GPIO
from time import sleep

servoPIN = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(31, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(servoPIN, GPIO.OUT)

freq = 50
left1 = GPIO.PWM(31, freq)
left2 = GPIO.PWM(32, freq)
right1 = GPIO.PWM(37, freq)
right2 = GPIO.PWM(38, freq)
pwmS = GPIO.PWM(servoPIN, 50)

left1.start(0)
left2.start(0)
right1.start(0)
right2.start(0)
pwmS.start(7)
sleep(0.1)
pwmS.ChangeDutyCycle(0)


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def set_camera(angle):
    angle = int(angle)
    if angle>=0 and angle<=5:
        angle = 90 + (angle*10)
    else:
        print("Valori accettati da 0 a 5")
        exit()
    duty = angle / 18 + 2
    GPIO.output(servoPIN, True)
    pwmS.ChangeDutyCycle(duty)
    sleep(0.4)
    GPIO.output(servoPIN, False)
    pwmS.ChangeDutyCycle(0)


def stop_pwm():
    left1.stop()
    left2.stop()
    right1.stop()
    right2.stop()
    pwmS.stop()
    GPIO.cleanup()


def traz(velocita, sterzo):
    if sterzo < 0:
        sterzo = -sterzo
        v_dx = velocita
        v_sx = map(sterzo, 0, 5, velocita, -velocita)
    else:
        v_dx = map(sterzo, 0, 5, velocita, -velocita)
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

