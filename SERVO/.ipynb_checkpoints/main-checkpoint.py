import time
import smbus
import PCA9685
import ServoPCA9685
import numpy as np

from math import *
import numpy as np

from math import *
import numpy as np

def rotate_y(theta, vec):


    # create rotation matrix
    rot_mat = np.array([[np.cos(theta), 0, np.sin(theta)],
                        [0,            1,            0],
                        [-np.sin(theta), 0, np.cos(theta)]])

    # perform rotation
    rotated_vec = rot_mat.dot(vec)

    return rotated_vec

def rotate_x(theta, vec):


    # create rotation matrix
    rot_mat = np.array([[ 1, 0           , 0           ],
                        [ 0, np.cos(theta),-np.sin(theta)],
                        [ 0, np.sin(theta), np.cos(theta)]])

    # perform rotation
    rotated_vec = rot_mat.dot(vec)

    return rotated_vec

def rotate_z(theta, vec):
    # convert angle to radians


    # create rotation matrix
    rot_mat = np.array([[ np.cos(theta), -np.sin(theta), 0 ],
                        [ np.sin(theta), np.cos(theta) , 0 ],
                        [ 0           , 0            , 1 ]])
    # perform rotation
    rotated_vec = rot_mat.dot(vec)

    return rotated_vec


def arm(x,y,z):
    l1 = 12
    l2 = 12.5
    offset_x = 4
    offset_y = 8
    theta = atan(z/x)

    vec = np.array([offset_x,offset_y,0])
    vec = rotate_y(-theta,vec)
    
    

    l0 = sqrt((x-vec[0])**2 + (y-vec[1])**2 + (z-vec[2])**2)

    if (l0+l1<=l2 or l1 >= l0+l2 or l0 > l1+l2):
        raise "NOT TODAY"
    v_bet = atan((y-offset_y)/sqrt((x-vec[0])**2+(z-vec[2])**2))

    alpha = acos((l0**2+l1**2-l2**2)/(2*l0*l1)) + v_bet
    
    beta = acos((l2**2+l1**2-l0**2)/(2*l2*l1))


    return theta,alpha,beta





class Manipulator:
    def __init__(self):
        i2cBus = smbus.SMBus(3)
        pca9685 = PCA9685.PCA9685(i2cBus)
        #self.servo00 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL00) # bottom
        self.servo01 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL01) # f
        # self.servo02 = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL02) # s
    
    def goto(self, x, y, z):
        params = {
            "dx": 4.5,
            "dz": 6,
            "x_dst": x,
            "y_dst": y, 
            "z_dst": z,
            "l1": 11,
            "l2": (2, 16.5)
        }
        p, a,b = arm(x, y ,z)
        #self.servo00.set_angle(p)
        self.servo01.set_angle(a)
        #self.servo02.set_angle(b)
        time.sleep(5)


m = Manipulator()
m.goto(1, 20, 1)
