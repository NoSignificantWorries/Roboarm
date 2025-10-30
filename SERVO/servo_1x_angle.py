
import time
import smbus
import PCA9685
import ServoPCA9685

i2cBus = smbus.SMBus(3)
pca9685 = PCA9685.PCA9685(i2cBus)
servo00 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL00)


# 0 - > 180
for angle in range(0, 18000 + 1):
    servo00.set_angle(angle)
    time.sleep(0.01)

# 180 -> 0
for angle in reversed(range(0, 180 + 1)):
    servo00.set_angle(angle)
    time.sleep(0.01)

servo00.disable()
