import numpy as np


def rot_x(x):
    return np.array([[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]], dtype=np.float32)


def rot_y(y):
    return np.array([[np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]], dtype=np.float32)


def rot_z(z):
    return np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]], dtype=np.float32)


def euler_to_matrix(rx, ry, rz):
    return rot_z(rz) @ rot_y(ry) @ rot_x(rx)
