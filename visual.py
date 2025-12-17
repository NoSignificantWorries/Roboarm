import numpy as np
from scipy.interpolate import RBFInterpolator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


points_arm = np.array([
    [330, 430, 200],
    [285, 405, 180],
    [240, 430, 200],
    [350, 355, 155],
    [285, 350, 135],
    [220, 355, 155],
    [285, 370, 160]
])
points = np.array([
    [-1, 1],
    [0, 1],
    [1, 1],
    [-1, 0],
    [0, 0],
    [1, 0],
    [0, 0.5]
])

points_interpolator = RBFInterpolator(points, points_arm)

n = 100
m = 50
arr = np.zeros((3, m + 1, n + 1))
for i, pi in enumerate(np.linspace(0, 1, m + 1)):
    for j, pj in enumerate(np.linspace(-1, 1, n + 1)):
        p = points_interpolator(np.array([pj, pi]).reshape(1, -1))[0]
        arr[0, i, j] = p[0]
        arr[1, i, j] = p[1]
        arr[2, i, j] = p[2]

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(16, 4))

ax[0].imshow(arr[0], cmap="rainbow")
ax[0].set_title("Alpha")
ax[1].imshow(arr[1], cmap="rainbow")
ax[1].set_title("Beta")
ax[2].imshow(arr[2], cmap="rainbow")
ax[2].set_title("Gamma")

plt.tight_layout()
plt.savefig("res.png", dpi=200)

