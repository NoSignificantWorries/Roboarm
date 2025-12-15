# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
from SERVO import ServoPCA9685, PCA9685
import smbus
import time
import math
import numpy as np
import matplotlib.pyplot as plt


# %%
class ManipulatorManegment:
    def __init__(self, l1=15, l2=15, alpha=0, beta=0, gamma=0, x=0, y=0, z=0, r_offset=0, z_offset=0):
        self._l1 = l1
        self._l2 = l2
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma
        self._x = x
        self._y = y
        self._z = z
        self._r_offset = r_offset
        self._z_offset = z_offset
    
    def find_alpha(self):
        self._alpha = math.atan(self._y / (self._x + 1e-16))
        if self._x < 0:
            self._alpha += math.pi
        x_offset = math.cos(self._alpha) * self._r_offset
        y_offset = math.sin(self._alpha) * self._r_offset
        return x_offset, y_offset
            
    def rotate_alpha(self, alpha):
        self._alpha = alpha * math.pi / 180
        self._x = math.cos(self._alpha)
        self._y = math.sin(self._alpha)
        
    def get_alpha(self):
        alpha = self._alpha * 180 / math.pi
        if alpha > 180:
            alpha -= 360
        return alpha
    
    def find_gamma(self):
        # self._gamma = math.acos(((self._l1**2 + self._l2**2 - self._x**2 - self._y**2 - self._z**2) - 7.5) / (2 * self._l1 * self._l2))
        self._gamma = math.acos((self._l1**2 + self._l2**2 - self._x**2 - self._y**2 - self._z**2) / (2 * self._l1 * self._l2))
    
    def get_gamma(self):
        return self._gamma * 180 / math.pi
        
    def find_beta(self):
        self._beta = math.pi - math.acos((self._l1**2 - self._l2**2 + self._x**2 + self._y**2 + self._z**2) / (2 * self._l1 * math.sqrt(self._x**2 + self._y**2 + self._z**2 + 1e-16))) - math.asin(self._z / math.sqrt(self._x**2 + self._y**2 + self._z**2 + 1e-16))
        
    def get_beta(self):
        return self._beta * 180 / math.pi

    def find_solution(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z - self._z_offset
        
        x_offset, y_offset = self.find_alpha()
        self._x -= x_offset
        self._y -= y_offset
        
        self.find_gamma()
        self.find_beta()

    def draw_solution(self):
        colors = ['red', 'blue', 'm']
        figure1, ax = plt.subplots(subplot_kw={'projection': '3d'})

        r = math.sqrt(self._x**2 + self._y**2)
        
        theta = np.linspace(0, 2 * math.pi, 360)
        x_circle = r * np.cos(theta)
        y_circle = r * np.sin(theta)

        theta_arc = np.linspace(0, self._alpha)
        x_arc = 0.5 * r * np.cos(theta_arc)
        y_arc = 0.5 * r * np.sin(theta_arc)

        ax.plot(x_circle, y_circle, [0] * len(x_circle), colors[2])
        ax.plot([-1.5 * r, 1.5 * r], [0, 0], [0, 0], colors[2] + '-.')
        ax.plot([0, 0], [-1.5 * r, 1.5 * r], [0, 0], colors[2] + '-.')
        ax.plot([0, self._x], [0, self._y], 'm--')
        ax.plot(x_arc, y_arc, 'm:')
        ax.scatter(self._x, self._y, 0, c='r')

        x = -self._l1 * math.cos(self._beta) / math.sqrt(1 + math.tan(self._alpha)**2)
        y = x * math.tan(self._alpha)
        z = self._l1 * math.sin(self._beta)

        if self._x < 0:
            x *= -1
            y *= -1

        ax.plot([0, x], [0, y], [0, z], colors[0])
        
        ax.plot([x, self._x], [y, self._y], [z, self._z], colors[1])

        ax.scatter(self._x, self._y, self._z, c='m')

        min_x = math.floor(min(0, x, self._x)) - 1
        max_x = math.ceil(max(0, x, self._x)) + 1
        x_range = np.linspace(min_x, max_x, max_x - min_x + 1)

        min_y = math.floor(min(0, y, self._y)) - 1
        max_y = math.ceil(max(0, y, self._y)) + 1
        y_range = np.linspace(min_y, max_y, max_y - min_y + 1)

        min_xy = min(min_x, min_y)
        max_xy = max(max_x, max_y)
        xy_range = np.linspace(min_xy, max_xy, max_xy - min_xy + 1)

        min_z = math.floor(min(0, z, self._z)) - 1
        max_z = math.ceil(max(0, z, self._z)) + 1
        z_range = np.linspace(min_z, max_z, max_z - min_z + 1)

        min_ = min(*x_range, *y_range, *z_range)
        max_ = max(*x_range, *y_range, *z_range)
        _range = np.linspace(min_, max_, int(max_ - min_ + 1))
        
        ax.set_xlabel('x')
        ax.set_xticks(_range)
        ax.set_ylabel('y')
        ax.set_yticks(_range)
        ax.set_zlabel('z')
        ax.set_zticks(_range)

        plt.show()

        figure2, axes = plt.subplots(2, 2, figsize=(10, 10))
        plt.subplots_adjust(hspace=0.2, wspace=0.2)
        alpha = 0.5

        axes[0, 0].plot([0, y], [0, z], colors[0], alpha=alpha)
        axes[0, 0].plot([y, self._y], [z, self._z], colors[1], alpha=alpha)
        axes[0, 0].grid()
        axes[0, 0].set_xlabel('y')
        axes[0, 0].set_xticks(y_range)
        axes[0, 0].set_ylabel('z')
        axes[0, 0].set_yticks(z_range)

        axes[0, 1].plot([0, x], [0, z], colors[0], alpha=alpha)
        axes[0, 1].plot([x, self._x], [z, self._z], colors[1], alpha=alpha)
        axes[0, 1].grid()
        axes[0, 1].set_xlabel('x')
        axes[0, 1].set_xticks(x_range)
        axes[0, 1].set_ylabel('z')
        axes[0, 1].set_yticks(z_range)

        axes[1, 0].plot([0, x], [0, y], colors[0], alpha=alpha)
        axes[1, 0].plot([x, self._x], [y, self._y], colors[1], alpha=alpha)
        axes[1, 0].grid()
        axes[1, 0].set_xlabel('x')
        axes[1, 0].set_xticks(x_range)
        axes[1, 0].set_ylabel('y')
        axes[1, 0].set_yticks(y_range)

        axes[1, 1].plot([0, x * math.sqrt(1 + math.tan(self._alpha)**2)], [0, z], colors[0], alpha=alpha)
        axes[1, 1].plot([x * math.sqrt(1 + math.tan(self._alpha)**2), self._x * math.sqrt(1 + math.tan(self._alpha)**2)], [z, self._z], colors[1], alpha=alpha)
        
        r = 0.3 * self._l1
        theta_arc = np.linspace(math.pi, math.pi - self._beta)
        k = -1 if self._x < 0 else 1
        x_arc = r * np.cos(theta_arc) * k
        y_arc = r * np.sin(theta_arc)
        axes[1, 1].plot(x_arc, y_arc, 'm:')
        axes[1, 1].text((x_arc.max() + x_arc.min()) / 2, (y_arc.max() + y_arc.min()) / 2, f'β = {int(self.get_beta())}°', c='r', size=15)

        gamma_1 = math.acos((self._l1**2 + x**2 + y**2 - z**2) / (2 * self._l1 * math.sqrt(x**2 + y**2)))
        gamma_2 = self._gamma - gamma_1
        theta_arc = np.linspace(-gamma_1, gamma_2)
        x_arc = x * math.sqrt(1 + math.tan(self._alpha)**2) + r * np.cos(theta_arc) * k
        y_arc = z + r * np.sin(theta_arc)
        axes[1, 1].plot(x_arc, y_arc, 'm:')
        axes[1, 1].text((x_arc.max() + x_arc.min()) / 2, (y_arc.max() + y_arc.min()) / 2, f'γ = {int(self.get_gamma())}°', c='r', size=15)
        
        axes[1, 1].grid()
        axes[1, 1].set_xlabel('x, y')
        axes[1, 1].set_xticks(xy_range)
        axes[1, 1].set_ylabel('z')
        axes[1, 1].set_yticks(z_range)

        print(f'l1 = {math.sqrt(x**2 + y**2 + z**2)}')
        print(f'l2 = {math.sqrt((self._x - x)**2 + (self._y - y)**2 + (self._z - z)**2)}')

        plt.show()


# %%
i2cBus = smbus.SMBus(3)
pca9685 = PCA9685.PCA9685(i2cBus)
servo_alpha = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL00)
servo_beta = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL01)
servo_gamma = ServoPCA9685.ServoPCA9685(pca9685, PCA9685.CHANNEL02)

# %%
angle1 = 0
offset1 = 17

angle2 = 90
offset2 = 4.5

alpha_approximation = lambda angle: (angle - angle1) / (angle2 - angle1) * (offset2 - offset1) + offset1
beta_offset = 8
gamma_offset = 25

# %%
alpha = 45
real_alpha = alpha + alpha_approximation(alpha)
servo_alpha.set_angle(real_alpha * math.pi / 180)

# %%
beta = 90
real_beta = beta + beta_offset
servo_beta.set_angle(real_beta * math.pi / 180)

# %%
gamma = 90
gamma_offset = 25
real_gamma = gamma + gamma_offset
servo_gamma.set_angle(real_gamma * math.pi / 180)


# %%
def coord(x, y, z):
    hand = ManipulatorManegment(l1=13.5, l2=13.5, r_offset=3, z_offset=8)
    
    real_x = x
    real_y = y
    real_z = z
    
    hand.find_solution(real_x, real_y, real_z)
    
    alpha = hand.get_alpha()
    beta = hand.get_beta()
    gamma = hand.get_gamma()
    
    real_alpha = alpha + alpha_approximation(alpha)
    real_beta = beta + beta_offset
    real_gamma = gamma + gamma_offset
    
    servo_alpha.set_angle(real_alpha * math.pi / 180)
    servo_beta.set_angle(real_beta * math.pi / 180)
    servo_gamma.set_angle(real_gamma * math.pi / 180)
    
    # hand.draw_solution()
    
    print(f'alpha = {alpha:.2f}')
    print(f'beta = {beta:.2f}')
    print(f'gamma = {gamma:.2f}')


# %%
def take_place():
    alpha = 45
    real_alpha = alpha + alpha_approximation(alpha)
    servo_alpha.set_angle(real_alpha * math.pi / 180)
    beta = 90
    real_beta = beta + beta_offset
    servo_beta.set_angle(real_beta * math.pi / 180)
    gamma = 90
    gamma_offset = 25
    real_gamma = gamma + gamma_offset
    servo_gamma.set_angle(real_gamma * math.pi / 180)


# %%
take_place()

# %% [markdown]
# ## Буква Э

# %%
coord(1, 5, 6)

# %%
coord(2, 5, 5)

# %%
coord(1, 5, 5)

# %%
coord(2, 5, 5)

# %%
coord(1, 5, 4)

# %%
#Буква Ч

# %%
take_place()

# %%
coord(2.2, 5, 7)

# %%
coord(2.2, 5, 6)

# %%
coord(3, 5, 6)

# %%
coord(3, 5, 7)

# %%
coord(3, 5, 5)

# %%

# %%
