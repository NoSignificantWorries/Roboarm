import time
import smbus
import PCA9685
import ServoPCA9685

i2cBus = smbus.SMBus(3)
pca9685 = PCA9685.PCA9685(i2cBus)
servo00 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL15)


# 130 -> 510
for pulse in range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1):
    servo00.set_pulse(pulse)
    time.sleep(0.01)

# 510 -> 130
for pulse in reversed(range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1)):
    servo00.set_pulse(pulse)
    time.sleep(0.01)

servo00.disable()
