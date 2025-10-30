import time
import smbus
import PCA9685
import ServoPCA9685

i2cBus = smbus.SMBus(3)
pca9685 = PCA9685.PCA9685(i2cBus)
servo00 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL15)
servo01 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL00)
servo02 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL13)
servo03 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL12)

# 130 -> 510
#for pulse in range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1):

servo01.set_angle(80)
servo02.set_angle(80)
servo03.set_angle(80)
#    servo01.set_pulse(pulse)
#    servo02.set_pulse(pulse)
#    servo03.set_pulse(pulse)
#    time.sleep(0.01)
#servo00.set_angle(0)
# 510 -> 130
#for pulse in reversed(range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1)):
#    servo00.set_pulse(pulse)
#    servo01.set_pulse(pulse)
#    servo02.set_pulse(pulse)
#    servo03.set_pulse(pulse)
#    time.sleep(0.01)
# for pulse in range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1):
#     servo00.set_pulse(pulse)
#     time.sleep(0.01)

# for pulse in reversed(range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1)):
#     servo00.set_pulse(pulse)
#     time.sleep(0.01)
    
# for pulse in range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1):
#     servo01.set_pulse(pulse)
#     time.sleep(0.01)

# for pulse in reversed(range(ServoPCA9685.servo_min, ServoPCA9685.servo_max + 1)):
#     servo01.set_pulse(pulse)
time.sleep(1)

servo00.disable()
servo01.disable()
servo02.disable()
servo03.disable()