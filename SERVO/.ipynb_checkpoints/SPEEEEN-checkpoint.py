import smbus
import PCA9685
import ServoPCA9685

import time
import numpy as np


i2cBus = smbus.SMBus(3)
pca9685 = PCA9685.PCA9685(i2cBus)

#servo00 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL00) # ?
servo01 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL03) # ???
# servo02 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL02) # ?????


servo01.set_angle(0)
time.sleep(1)

angle = 5
count = 0

while True:
    #servo00.set_angle(angle)
    servo01.set_angle(angle)
    #servo02.set_angle(angle)

    angle = (angle + np.pi / 30) % np.pi
    count += 1

    print(f'{count} -- {angle}')
    time.sleep(1)
