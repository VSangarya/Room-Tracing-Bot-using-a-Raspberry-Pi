import RPi.GPIO as GPIO
import time
import os

t=0

def init():
    TRIG=16
    ECHO=18
    TRIG2=29
    ECHO2=31

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(ECHO2, GPIO.IN)
    GPIO.output(TRIG2, False)


def forward(tf):
   init()
   GPIO.output(7, False)
   GPIO.output(11, True)
   GPIO.output(13, True)
   GPIO.output(15 False)
   time.sleep(tf)
   GPIO.cleanup()

def reverse(tf):
   init()
   GPIO.output(7, True)
   GPIO.output(11, False)
   GPIO.output(13, False)
   GPIO.output(15, True)
   time.sleep(tf)
   GPIO.cleanup()

def left(tf):
   init()
   GPIO.output(7, False)
   GPIO.output(11, True)
   GPIO.output(13, False)
   GPIO.output(15, True)
   time.sleep(tf)
   GPIO.cleanup()

def right(tf):
   init()
   GPIO.output(7, True)
   GPIO.output(11, False)
   GPIO.output(13, True)
   GPIO.output(15, False)
   time.sleep(tf)
   GPIO.cleanup()

def none(tf):
   init()
   GPIO.output(7, False)
   GPIO.output(11, False)
   GPIO.output(13, False)
   GPIO.output(15, False)
   time.sleep(tf)
   GPIO.cleanup()

init()

TRIG=16
ECHO=18
TRIG2=29
ECHO2=31

print "Calibrating"
time.sleep(2)

print "Start"

def measure():
    global t
    i=0
    while True:
        print t
        t+=1
        if t==28:
            print 'End'
            os._exit(0)
        init()
        print 'S1'
        GPIO.output(TRIG, True)
        time.sleep(0.0000002)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            pulse_start=time.time()
        print 'S2'

       while GPIO.input(ECHO)==1:
            pulse_end=time.time()
        print 'S3'

        pulse_duration=pulse_end-pulse_start
        distance=pulse_duration*17150
        distance=round(distance+1.15,2)
        print 'S4'

        with open('text1.txt','a') as f:
            if distance<=20 and distance>=8.5:
                 print "Distance",distance,"cm"
                 with open('text1.txt','a') as f:
                     print >> f, 'turtle.forward(15)
                 i=1
                forward(0.7)
                measure()

            if distance>20:
                print "Distance",distance,"cm"
                with open('text1.txt','a') as f:
                    print >> f,'turtle.forward(15)'

                i=1
                forward(0.7)
                measure2()

            if distance<=8.5:
                print "Too close"
                i=0
                reverse(0.35)
                time.sleep(0.2)
                left(0.9)
                forward(0.7)
                with open('text1.txt','a') as f:
                    print >> f,'turtle.left(90)'
        time.sleep(0.2)


def measure2():
    i=0
    while True:
        init()
        GPIO.output(TRIG2,True)
        time.sleep(0.001)
        GPIO.output(TRIG2, False)
        while GPIO.input(ECHO2)==0:
            pulse_start2=time.time()
        while GPIO.input(ECHO2)==1:
             pulse_end2=time.time()
        pulse_duration2=pulse_end2-pulse_start2
        distance2=pulse_duration2*17150
        distance2=round(distance2+1.15,2)

        if distance2>=40:
            print "Distance right",distance2,"cm"
            i=1
            forward(0.35)
            right(0.95)
            forward(0.2)
            with open('text1.txt','a') as f:
                print >> f, 'turtle.right(90)'
             break

        if distance2<40:
            print "Distance right",distance2,"cm"
            i=0
            none(0.1)
            break
 
with open('text1.txt','w') as f:
    print " "

measure()
GPIO.cleanup()
