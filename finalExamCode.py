#!/usr/bin/python
# Josie Foley
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
def magnitude(number):
    absolute = math.sqrt((number[0] * number[0]) + (number[1] * number[1]))
    return absolute
def complex_division(complex_a, complex_b):
    real_answer = complex_a[0] / complex_b[0]
    imag_answer = complex_a[1] - complex_b[1]
    return real_answer, imag_answer

def complex_multiplication(complex_a, complex_b):
    real_answer = complex_a[0] * complex_b[0]
    imag_answer = complex_a[1] + complex_b[1]
    return real_answer, imag_answer

try:
    capConnected = True
    while True:

    frequency = input('\nWhat is the frequency of the source? (in Hz): ')
    voltage = input('\nWhat is the voltage of the source? (in RMS): ')
    resistor_value = input('\nWhat value of resistor is present? (in Ohms): ')
    inductor_value = input('\nWhat is the value of your inductor? (in Henrys): ')
    inductor_resistance = input('\nWhat is the resistance of the wiring of the inductor? (in Ohms): ')
    capacitor_value = input('\nWhat is the value of your capacitor? (in Farads): ')

# Some basic calculations
    omega = 2 * pi * frequency
    total_resistance = inductor_resistance + resistor_value
    inductance = omega * inductor_value
    mag_inductance = (inductor_resistance, inductance)
    mag_inductance = magnitude(mag_inductance)
    capacitance = (1/(omega * capacitor_value))
    impedance = total_resistance, (inductance + -capacitance)
    mag_impedance = magnitude(impedance)
    current = float(voltage) / float(mag_impedance)
    v_r = current * resistor_value
    v_l = current * inductance
    v_c = current * capacitance

# Phase Angle
    if inductance > capacitance:
        argument_send = impedance[1] / impedance[0]
    else:
        if capacitance > inductance:
            argument_send = impedance[0] / impedance[1]
        else:
            argument_send = 0
    phase_radians = math.atan(argument_send)
    phase_angle = phase_radians * 180/pi
        if capConnected:
            # calculate the full magnitude and phase of the parallel circuit here
            if total_impedance[1] > 0:
                print('Current will be lagging voltage by %f degrees' % total_impedance[1])
            if total_impedance[1] < 0:
                print('Current will be leading voltage by %f degrees' % total_impedance[1])
            if total_impedance[1] == 0:
                print('Voltage and current will be in phase!')
    #print('Total current will be %f A' % total_current)
            magnitude = phase = 1

        else:
            # here is where the magnitude and phase of just the inductor, since the cap is disconnected by the switch
            mag_inductance = (inductor_resistance, inductance)
            mag_inductance = magnitude(mag_inductance)
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
