#!/usr/bin/python
# dframe
""" This is a program that will calculate the impedance based on the schematic:
https://sites.google.com/site/reflectiondetection/vinu/FinalExamCircuit2.png

The goal:  Calculate the impedance, from A to B, once a second, displayed on the LCD.
Assume that the pushbutton is inactive, both connections are made, and the capacitor
is connected in parallel with the inductor.

When the pushbutton is activated, remove the capacitor from the impedance calculation. still
posting the impedance once a second.  When the pushbutton is inactivated, recalculate the
impedance and post it once a second, again like above.
The script is based on code from the following RaspPi.tv site:
"""
# script by Alex Eames http://RasPi.tv/
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio


import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

GPIO_INTERRUPT_PIN = 18
L1 = 2.5E-3 # Henrys
R1 = 25     # Ohms
C1 = 100E-9 # Farads
FREQ = 10E3 # Hertz

lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_INTERRUPT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def check4edge(pin):
    """ This will return a False for a falling edge and a True for a rising edge"""
    if GPIO.input(pin):
        GPIO.remove_event_detect(pin)
        GPIO.wait_for_edge(pin, GPIO.FALLING, bouncetime=200)
        return False
    else:
        GPIO.remove_event_detect(pin)
        GPIO.wait_for_edge(pin, GPIO.RISING, bouncetime=200)
        return True


try:
    capConnected = True
    while True:
        # this is where you solve the circuit.  Please post the impedance between point A
        # and B, every time the button is pressed or released. If the button is being pressed
        # the impedance without the capacitance.
        if capConnected:
            # calculate the full magnitude and phase of the parallel circuit here
            magnitude = phase = 1

        else:
            # here is where the magnitude and phase of just the inductor, since the cap is disconnected by the switch
            magnitude = phase = 2
            capConnected = True

        impedance = "Impedance:\n(%3.3f, %3.3f)\n" % (magnitude, phase)
        lcd.home()
        lcd.message(impedance)
        capConnected = check4edge(GPIO_INTERRUPT_PIN)
except KeyboardInterrupt:
    lcd.clear()
    lcd.message("Program\nStopped")
finally:
    GPIO.cleanup()  # clean up GPIO on exit
