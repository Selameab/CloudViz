# CloudViz

Simple point cloud visualizer for debugging 3D object detectors.

Installation
============

Dependencies

```shell
sudo apt install python3-pyqt5
```

Clone and install

```shell
git clone https://github.com/Selameab/CloudViz
pip install CloudViz
```

Usage
=========

```python
import numpy as np
import time
from cloudviz import Visualizer

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
```

Keyboard Shortcuts
-------------------

<kbd>K</kbd> Set current viewpoint as default

<kbd>Q</kbd> Quit

<kbd>R</kbd> Reset viewpoint