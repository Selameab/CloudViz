import time
from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager

import matplotlib.cm as cm
import numpy as np
from PyQt5 import QtWidgets, QtCore
from matplotlib.colors import Normalize

from cloudviz.cloud_vw import CloudViewWidget
from cloudviz.dtypes import IPCData


class Visualizer:
    def __init__(self, title='CloudViz', window_size=(1200, 675), pt_size=2, background_color=(0, 0, 0)):
        BaseManager.register('IPCData', IPCData)
        base_manager = BaseManager()
        base_manager.start()
        # noinspection PyUnresolvedReferences
        self.ipc_data = base_manager.IPCData()

        self.last_key_pressed = Value('i', 0)

        self.viz_process = Process(target=_VizProcess, args=(title, window_size, pt_size, background_color, self.ipc_data, self.last_key_pressed),
                                   daemon=True)
        self.viz_process.start()

    def plot(self, pts=None, pts_color=None, boxes=None, boxes_color=None, texts=None):
        """
        :param pts:
        :param pts_color:
        :param boxes:
        :param boxes_color:
        :param texts:
        :return:
        """
        self.ipc_data.set(pts, pts_color, boxes, boxes_color, texts)

    def get_key(self):
        self.last_key_pressed.value = 0
        while self.last_key_pressed.value == 0:
            time.sleep(0.001)
        return self.last_key_pressed.value


class _VizProcess:
    def __init__(self, title, window_size, pt_size, background_color, ipc_data, last_key_pressed):
        self.ipc_data = ipc_data
        self.last_key_pressed = last_key_pressed

        app = QtWidgets.QApplication([])

        self.vw = CloudViewWidget(last_key_pressed=last_key_pressed)
        self.vw.pt_size = pt_size
        self.vw.setBackgroundColor(*background_color)
        self.vw.setMinimumSize(*window_size)
        self.vw.setWindowTitle(title)
        self.vw.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__refresh)
        self.timer.start(30)  # Refresh render every 20ms

        app.exec()

    def __refresh(self):
        self.vw.plot(**self.ipc_data.get())


class ColorMap:
    def __init__(self, values, cmap='hsv'):
        vmin, vmax = (np.percentile(values, 0.05), np.percentile(values, 99.5))
        self.cm = cm.ScalarMappable(norm=Normalize(vmin=vmin, vmax=vmax), cmap=cmap)

    def paint(self, v):
        return self.cm.to_rgba(v)


def main():
    viz = Visualizer()
    cmap = ColorMap([-5, 5])

    while True:
        pts = np.random.uniform(-5, 5, (1000, 3))
        pts_color = cmap.paint(pts[:, 0])

        viz.plot(
            pts=pts,
            pts_color=pts_color,
            boxes=[[2, 1, 0, 5, 2, 1, 0.1, 0.2, 0.8], [5, -4.1, 0.2, 4, 1.2, 1.5, 0, 0, -0.4]],
            boxes_color=[[1.0, 1.0, 0.2, 1.0], [0.2, 0.9, 0.8, 1.0]],
            texts=[[0, 0, 0, "Origin"], [2, 1, 0, "Box 1"]]
        )
        print(viz.get_key())
        # time.sleep(1)


if __name__ == '__main__':
    main()
