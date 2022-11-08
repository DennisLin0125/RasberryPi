import RPi.GPIO as gpio
import time

'''
GPIO.BOARD 選項是指定在電路版上接脚的號碼
GPIO.BCM 選項是指定GPIO後面的號碼
'''

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
 
pin = [29, 31, 33, 35]
for i in range(4):
    gpio.setup(pin[i], gpio.OUT)
 
forward_sq = ['0011', '1001', '1100', '0110']
reverse_sq = ['0110', '1100', '1001', '0011']
 
def forward(steps, delay):
    for i in range(steps):
        for step in forward_sq:
            set_motor(step)
            time.sleep(delay)
 
def reverse(steps, delay):
    for i in range(steps):
        for step in reverse_sq:
            set_motor(step)
            time.sleep(delay)
 
def set_motor(step):
    for i in range(4):
        gpio.output(pin[i], step[i] == '1')
 
try:
    while True:
        set_motor('0000')
        forward(360, 0.005)
        set_motor('0000')
        reverse(360,0.005)
except KeyboardInterrupt:
    gpio.cleanup()
