import LCD1602
import time
import random
from gpiozero import PWMLED
from signal import pause

led = PWMLED(21)

led.pulse()


LCD1602.init(0x27, 1)   # init(slave address, background light)
LCD1602.write(0, 0, 'Hi....')
LCD1602.write(0, 1, 'Start Log data!')
time.sleep(2)

try:
    print('Press Ctrl-C To Stop')
    LCD1602.clear()
    while True:
        # LCD1602.write(0, 0,"Date: {}".format(time.strftime("%Y/%m/%d")))
        v=random.randint(600,700)
        i=random.randint(15,20)
        myTime=time.strftime("%H:%M:%S")
        LCD1602.write(0, 0,f"V:{v}V")
        LCD1602.write(0, 1,f"I: {i}A")
        LCD1602.write(8, 0,f"P:{v*i:05d}W")
        LCD1602.write(8, 1,f"{myTime}")
        time.sleep(0.2)
except KeyboardInterrupt:
    print('Close Program')
    LCD1602.clear()
finally:
    LCD1602.clear()