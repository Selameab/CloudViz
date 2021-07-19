import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtGui, QtCore, QtWidgets
from cloudviz.transforms import euler_to_matrix


class CloudViewWidget(gl.GLViewWidget):
    def __init__(self, parent=None, last_key_pressed=None):
        super(CloudViewWidget, self).__init__(parent)

        self.last_key_pressed = last_key_pressed

        self.texts = []
        self.paintGL = self.__paint_gl

        self.qt_settings = QtCore.QSettings('CloudViz', 'CloudViz')

        self.setBackgroundColor(0, 0, 0)
        self.pt_size = 3

        self.__reset_camera()
        self.plot()

    def __paint_gl(self, *args, **kwargs):
        gl.GLViewWidget.paintGL(self, *args, **kwargs)
        self.qglColor(QtGui.QColor(255, 255, 255, 255))
        for item in self.texts:
            self.renderText(*item)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_K:
            self.qt_settings.setValue('camera_params', {
                'distance': self.opts['distance'],
                'elevation': self.opts['elevation'],
                'azimuth': self.opts['azimuth'],
                'center': (self.opts['center'].x(), self.opts['center'].y(), self.opts['center'].z())
            })
            print("The following params were saved", self.opts)

        elif event.key() == QtCore.Qt.Key_Q:
            QtWidgets.qApp.quit()
        elif event.key() == QtCore.Qt.Key_R:
            self.__reset_camera()
        else:
            self.last_key_pressed.value = event.key()

    def __reset_camera(self):

        distance, elevation, azimuth, pos = 34.2, 2, -180, (1.5, -0.12, 4.5)
        if self.qt_settings.value('camera_params') is not None:
            opts = self.qt_settings.value('camera_params')
            distance, elevation, azimuth, pos = opts['distance'], opts['elevation'], opts['azimuth'], opts['center']
        self.setCameraPosition(distance=distance, elevation=elevation, azimuth=azimuth, pos=pg.Vector(*pos))
        self.opts['fov'] = 40

    def __draw_lines(self, v, thickness: int, color: list):
        """
        :param v: vertices of the line segment
        :param thickness: thickness of the line
        :param color: color defined as a list [r, g, b, a]
        :return:
        """
        self.addItem(gl.GLLinePlotItem(pos=np.array(v), mode='line_strip', color=color, width=thickness, antialias=True))

    def __draw_coordinate_frame(self, xyz=(0, 0, 0), scale=0.25, thickness=2):
        pts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32) * scale
        pts += xyz

        self.__draw_lines(pts[[0, 1]], thickness, [1.0, 0, 0, 1.0])
        self.__draw_lines(pts[[0, 2]], thickness, [0, 1.0, 0, 1.0])
        self.__draw_lines(pts[[0, 3]], thickness, [0, 0, 1.0, 1.0])

    def __draw_box(self, box: np.array, color):
        """
        :param box:
        :return:
        """
        dx, dy, dz = box[3:6]
        corners = np.array([
            [dx / 2, dx / 2, dx / 2, dx / 2, -dx / 2, -dx / 2, -dx / 2, -dx / 2],
            [dy / 2, dy / 2, -dy / 2, -dy / 2, dy / 2, dy / 2, -dy / 2, -dy / 2],
            [dz / 2, -dz / 2, dz / 2, -dz / 2, dz / 2, -dz / 2, dz / 2, -dz / 2],
        ], dtype=np.float32).T

        corners = corners @ (euler_to_matrix(*box[6:9])).T + box[:3]

        for segment in [[5, 6, 7, 5, 4], [7, 3, 1, 5], [3, 2, 0, 1], [2, 6, 4, 0]]:
            self.__draw_lines([corners[c] for c in segment], thickness=2, color=color)

    @staticmethod
    def __get_color(colors, i, default_color):
        if colors is None:
            return default_color
        if isinstance(colors, list):
            return colors[i]
        return colors

    def clear(self):
        self.texts = []
        self.items.clear()
        self.update()

    def plot(self, pts=None, pts_color=None, boxes=None, boxes_color=None, texts=None):
        """
        :param pts:
        :param pts_color:
        :param boxes:
        :param boxes_color:
        :param texts:
        :return:
        """
        self.clear()

        self.__draw_coordinate_frame()
        if pts is not None and len(pts) > 0:
            pi = gl.GLScatterPlotItem(pos=pts, size=self.pt_size, color=(0.4, 1.0, 0.2, 1.0) if pts_color is None else pts_color)
            pi.setGLOptions('opaque')
            self.addItem(pi)

        if boxes is not None and len(boxes) > 0:
            for i in range(len(boxes)):
                self.__draw_box(boxes[i], self.__get_color(boxes_color, i, (1.0, 0.4, 0.1, 1.0)))

        if texts is not None and len(texts) > 0:
            self.texts = texts
