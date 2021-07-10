from multiprocessing import Process
from multiprocessing.managers import BaseManager

from PyQt5 import QtWidgets, QtCore

from cloudviz.cloud_vw import CloudViewWidget

from cloudviz.dtypes import IPCData


class Visualizer:
    def __init__(self, title='CloudViz', window_size=(1200, 675)):
        BaseManager.register('IPCData', IPCData)
        manager = BaseManager()
        manager.start()
        # noinspection PyUnresolvedReferences
        self.ipc_data = manager.IPCData()

        self.viz_process = Process(target=_VizProcess, args=(title, window_size, self.ipc_data), daemon=True)
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


class _VizProcess:
    def __init__(self, title, window_size, ipc_data):
        self.ipc_data = ipc_data

        app = QtWidgets.QApplication([])

        self.vw = CloudViewWidget()
        self.vw.setMinimumSize(*window_size)
        self.vw.setWindowTitle(title)
        self.vw.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__refresh)
        self.timer.start(30)  # Refresh render every 20ms

        app.exec()

    def __refresh(self):
        self.vw.plot(**self.ipc_data.get())


def main():
    import numpy as np
    import time
    viz = Visualizer()
    while True:
        viz.plot(
            pts=np.random.uniform(-5, 5, (1000, 3)),
            pts_color=np.random.uniform(0, 1, (1000, 4)),
            boxes=[[2, 1, 0, 5, 2, 1, 0.1, 0.2, 0.8], [5, -4.1, 0.2, 4, 1.2, 1.5, 0, 0, -0.4]],
            boxes_color=[[1.0, 1.0, 0.2, 1.0], [0.2, 0.9, 0.8, 1.0]],
            texts=[[0, 0, 0, "Origin"], [2, 1, 0, "Box 1"]]
        )
        time.sleep(1)


if __name__ == '__main__':
    main()
