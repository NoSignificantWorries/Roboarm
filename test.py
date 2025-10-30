# %%
import numpy as np

# %%
d_1 = 10
d_2 = 8

d90 = np.pi / 2
d180 = np.pi

a_1 = (-d90, d90)
a_2 = (0, d180)
a_3 = (-d90, d90)

# %%
teta_1, teta_2, teta_3 = 0, d90, 0

# %%
def pose_by_rot(alpha, betta, gamma, d1, d2):
    x_2, y_2 = np.cos(betta) * d1, np.sin(betta) * d1
    x_3, y_3 = np.cos(gamma) * d2, np.sin(gamma) * d2
    
    x_4, y_4 = x_2 + x_3, y_2 + y_3
    
    x_5, y_5 = np.cos(alpha) * x_4, np.sin(alpha) * x_4
    z = y_4
    print(x_5, y_5, z)


pose_by_rot(teta_1, teta_2, teta_3, d_1, d_2)

# %%
class Robot:
    def __init__(self, d_1, d_2, a_1, a_2, a_3, teta_1: float = 0, teta_2: float = 0, teta_3: float = 0) -> None:
        self.d = np.array([[d_1], [d_2]])
        self.angles = (teta_1, teta_2, teta_3)

        self.a_1 = a_1
        self.a_2 = a_2
        self.a_3 = a_3

        self.pos = self.rot(*self.angles)

    def rot(self, teta_1, teta_2, teta_3):
        rot = np.array([[np.cos(teta_2), np.cos(teta_3)],
                        [np.sin(teta_2), np.sin(teta_3)]])
        
        vec_ = rot @ self.d
        x_ = vec_[0, 0]
        
        x, y = np.cos(teta_1) * x_, np.sin(teta_1) * x_
        z = vec_[1, 0]

        return np.array([x, y, z])

    def to_point(self, point):
        x, y, z = point[0], point[1], point[2]

        teta_1 = np.arctan2(y, x)
        x_ = np.hypot(x, y)

        d1, d2 = self.d[0, 0], self.d[1, 0]
        R = np.hypot(x_, z)
    
        if R > d1 + d2 or R < abs(d1 - d2):
            raise ValueError("Point is unreacheble")
        
        cos_phi = (d1**2 + d2**2 - R**2) / (2 * d1 * d2)
        cos_phi = np.clip(cos_phi, -1.0, 1.0)
        phi = np.arccos(cos_phi)
        
        
        cos_beta = (d1**2 + R**2 - d2**2) / (2 * d1 * R)
        cos_beta = np.clip(cos_beta, -1.0, 1.0)
        beta = np.arccos(cos_beta)
        
        teta_2 = teta_1 - beta
        teta_3 = teta_2 + phi
        
        return np.array([teta_1, teta_2, teta_3])
        


# %%
robot = Robot(10, 8, (), (), (), 0, d90, 0)

print(robot.pos)

point = np.array([2, 2, 2])
robot.rot(*robot.to_point(point))


