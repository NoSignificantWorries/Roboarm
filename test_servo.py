import time
import smbus
from SERVO import ServoPCA9685, PCA9685

# Инициализация I2C шины (номер зависит от Raspberry Pi версии)
i2cBus = smbus.SMBus(3)  # Для RPi 3/4 обычно используется 1

# Создание объекта PCA9685
pca9685 = PCA9685.PCA9685(i2cBus)

# Инициализация сервоприводов на каналах
servo_alpha = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL00)
servo_beta = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL01)
servo_gamma = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL02)

servo_alpha.set_pulse(300)
time.sleep(0.01)

