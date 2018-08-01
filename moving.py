# Servo Control

import time
import wiringpi
 
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
 
# set #18 and #13 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(13, wiringpi.GPIO.PWM_OUTPUT)
 
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)



def move(pulse,servo):
        """
        Here we define which servo
        should move and by how much"""
        #pulse=(50+200*float(angle)/180)
        wiringpi.pwmWrite(servo, pulse)