import numpy as np
import matplotlib.pyplot as plt

pa = np.array([0, 0])  # Position of the single-anchor

real_traj = np.array([[10, -10], [6, -8]])  # Actual trajectory of the mobile unit

move_vector = real_traj[1] - real_traj[0]
heading = np.mod(np.arctan2(move_vector[1], move_vector[0]), 2 * np.pi)
distance = np.sqrt(np.sum((pa - real_traj[1]) ** 2))

dx1 = 0.1  # X-axis resolution
dx2 = 0.1  # Y-axis resolution

x1 = np.arange(-13, 14, dx1)
x2 = np.arange(-13, 14, dx2)
X1, X2 = np.meshgrid(x1, x2)
X = np.column_stack((X1.flatten(), X2.flatten()))  # Coordinates of 2-D plane

sigma_h = 20 * (np.pi / 180)  # std deviation for heading measurements
sigma_d = 1  # std deviation for distance measurements between user and single-anchor

d_pdf = (1 / (np.sqrt(2 * np.pi) * sigma_d)) * np.exp(
    -0.5 * (1 / (sigma_d ** 2)) * (distance - np.sqrt((X1 - pa[0]) ** 2 + (X2 - pa[1]) ** 2)) ** 2
)

d_pdf = (1 / np.sum(d_pdf)) * d_pdf

n_Row, n_Col = d_pdf.shape
h_pdf = np.zeros((n_Row, n_Col))

for i in range(n_Row):
    for j in range(n_Col):
        diff = heading - np.mod(np.arctan2(X2[i, 0] - real_traj[0, 1], X1[0, j] - real_traj[0, 0]), 2 * np.pi)
        if np.abs(diff) < np.pi:
            h_pdf[i, j] = (1 / (np.sqrt(2 * np.pi) * sigma_h)) * np.exp(-0.5 * (1 / (sigma_h ** 2)) * diff ** 2)
        elif diff < -np.pi:
            h_pdf[i, j] = (1 / (np.sqrt(2 * np.pi) * sigma_h)) * np.exp(
                -0.5 * (1 / (sigma_h ** 2)) * (diff + 2 * np.pi) ** 2
            )
        elif diff > np.pi:
            h_pdf[i, j] = (1 / (np.sqrt(2 * np.pi) * sigma_h)) * np.exp(
                -0.5 * (1 / (sigma_h ** 2)) * (diff - 2 * np.pi) ** 2
            )

h_pdf = (1 / np.sum(h_pdf)) * h_pdf

post_pdf = h_pdf * d_pdf
post_pdf = (1 / np.sum(post_pdf)) * post_pdf

h_pdf_rest = np.zeros((n_Row, n_Col))
l_max = 6

for i in range(n_Row):
    for j in range(n_Col):
        if np.sqrt((X1[0, j] - real_traj[0, 0]) ** 2 + (X2[i, 0] - real_traj[0, 1]) ** 2) <= l_max:
            h_pdf_rest[i, j] = h_pdf[i, j]
        else:
            h_pdf_rest[i, j] = 0

post_pdf_rest = h_pdf_rest * d_pdf
post_pdf_rest = (1 / np.sum(post_pdf_rest)) * post_pdf_rest

maximum = np.max(post_pdf_rest)
row, col = np.where(post_pdf_rest == maximum)
Possible_Point = [dx1 * (col + (x1[0] / dx1) - 1), dx2 * (row + (x2[0] / dx2) - 1)]


fig = plt.figure()
ax = fig.add_subplot(111)
f = ax.pcolor(X1, X2, h_pdf)
plt.colorbar(f, ax=ax)
ax.set_xlabel('$x$-axis (m)', fontsize=12)
ax.set_ylabel('$y$-axis (m)', fontsize=12)
ax.scatter(real_traj[0, 0], real_traj[0, 1], c='b', marker='o', label='Start')
ax.scatter(pa[0], pa[1], c='g', marker='o', label='Anchor')
ax.set_aspect('equal')
ax.set_title('PDF of Heading')
ax.legend()

fig = plt.figure(2)
ax = fig.add_subplot(111)
f = ax.pcolor(X1, X2, h_pdf_rest)
plt.colorbar(f, ax=ax)
ax.set_xlabel('$x$-axis (m)', fontsize=12)
ax.set_ylabel('$y$-axis (m)', fontsize=12)
ax.scatter(real_traj[0, 0], real_traj[0, 1], c='b', marker='o', label='Start')
ax.scatter(pa[0], pa[1], c='g', marker='o', label='Anchor')
ax.set_aspect('equal')
ax.set_title('PDF of Restricted Heading')
ax.legend()

fig = plt.figure(3)
ax = fig.add_subplot(111)
f = ax.pcolor(X1, X2, d_pdf)
plt.colorbar(f, ax=ax)
ax.set_xlabel('$x$-axis (m)', fontsize=12)
ax.set_ylabel('$y$-axis (m)', fontsize=12)
ax.scatter(real_traj[0, 0], real_traj[0, 1], c='b', marker='o', label='Start')
ax.scatter(pa[0], pa[1], c='g', marker='o', label='Anchor')
ax.set_aspect('equal')
ax.set_title('PDF of Distance')
ax.legend()

fig = plt.figure(5)
ax = fig.add_subplot(111)
f = ax.pcolor(X1, X2, post_pdf_rest)
plt.colorbar(f, ax=ax)
ax.set_xlabel('$x$-axis (m)', fontsize=12)
ax.set_ylabel('$y$-axis (m)', fontsize=12)
ax.scatter(real_traj[0, 0], real_traj[0, 1], c='b', marker='o', label='Start')
ax.scatter(pa[0], pa[1], c='g', marker='o', label='Anchor')
ax.scatter(Possible_Point[0], Possible_Point[1], c='r', marker='o', label='Estimate')
ax.set_aspect('equal')
ax.set_title('Restricted Posterior PDF')
ax.legend()

#plt.show()