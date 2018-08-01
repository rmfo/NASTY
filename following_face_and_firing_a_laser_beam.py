###############################################################################
#                                                                             #
#                                                                             #
#                                                                             #
# credit: Andre Heil  - avh34                                                 #
#          Jingyao Ren - jr386                                                #
#                                                                             #
# date:    December 1st 2015,                                                 #
#                                                                             #
# brief:   The logic of the code was borrowed, but adapted and rewritten      #
#                                                                             #
###############################################################################


### Imports ###################################################################

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
from moving import move #a simple script containing a function to move servos
import RPi.GPIO as GPIO


### Setup #####################################################################
GPIO.setmode(GPIO.BCM)
# setup pin 23 as an output
GPIO.setup(23,GPIO.OUT)



# Center coordinates <- defined with 0 at the top left corner if you look at the camera
cx = 160
cy = 120

# Setting the initial position for the servos
xdeg = 150
ydeg = 180

#putting servos to the initial position
move(xdeg,13)
move(ydeg,18)

# Setup the camera
camera = PiCamera()
camera.resolution = ( 320, 240 )
camera.framerate = 60
rawCapture = PiRGBArray( camera, size=( 320, 240 ) )

# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml' )



### Main ######################################################################

# Capture frames from the camera
for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):

    image = frame.array

    # Use the cascade file we loaded to detect faces
    gray = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    faces = face_cascade.detectMultiScale( gray )

    


    # Draw a rectangle around every face and move the motor towards the face
    for ( x, y, w, h ) in faces:

        cv2.rectangle( image, ( x, y ), ( x + w, y + h ), ( 100, 255, 100 ), 2 )
        cv2.putText( image, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

        tx =x + w/2
        ty =y + h/2
        print "Coordinates: x:" + str( tx ) + "y:" +str(ty)
        print "diff from center x:"+ str(cx - tx)+"diff from center y"+str(cy-ty)

        # if close enough to the face, turn on the laser
        if abs(cy-ty)<10 and abs(cx-tx)<10:
            GPIO.output(23,True)
        else:
            GPIO.output(23,False)

        #move with different speed according to the distance

            ##horisontal axis

        if abs(cx-tx)>10:
            if   ( cx - tx >  3 and xdeg <= 247 ):
                xdeg += 2
                move(xdeg,13)
            elif ( cx - tx < -3 and xdeg >= 3 ):
                xdeg -= 2
                move(xdeg,13)
        else:
            if   ( cx - tx >  3 and xdeg <= 247):
                xdeg += 2
                move(xdeg,13)
            elif ( cx - tx < -3 and xdeg >= 3 ):
                xdeg -= 2
                move(xdeg,13)

            ##vertical axis

        if abs(cy-ty)>10:
            if   ( cy - ty >  1 and ydeg >= 70 ):
                ydeg -= 1
                move(ydeg,18)
            elif ( cy - ty < -1 and ydeg <= 247 ):
                ydeg += 1
                move(ydeg,18)
        else: 
            if   ( cy - ty >  1 and ydeg >= 70 ):
                ydeg -= 1
                move(ydeg,18)
            elif ( cy - ty < -1 and ydeg <= 247):
                ydeg += 1
                move(ydeg,18) 

    if xdeg<3 or xdeg>247 or ydeg<3 or ydeg>247:

        cv2.putText( image, "TARGET ESCAPED", ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )



    # Show the frame
    cv2.imshow( "Frame", image )
    cv2.waitKey( 1 )

    # Clear the stream in preparation for the next frame
    rawCapture.truncate( 0 )