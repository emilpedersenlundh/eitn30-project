#!/home/fideloper/.envs/eitn30-project/bin/python3

import sys
import RPi.GPIO as GPIO

GPIO_TYPES = {
    GPIO.IN: 'Input',
    GPIO.OUT: 'Output',
    GPIO.SPI: 'SPI',
    GPIO.I2C: 'I2C',
    GPIO.HARD_PWM: 'PWM',
    GPIO.SERIAL: 'Serial',
    GPIO.UNKNOWN: 'Unknown'
}

def listFunctions():
    GPIO.setmode(GPIO.BCM)
    for i in range(1, 28):
        print("{}{}{}{}".format("GPIO ", i, ": ", GPIO_TYPES[GPIO.gpio_function(i)]))

if __name__ == "__main__":
    listFunctions()
