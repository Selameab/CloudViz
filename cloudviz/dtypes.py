class IPCData:
    def __init__(self):
        self.pts = None
        self.pts_color = None
        self.boxes = None
        self.boxes_color = None
        self.texts = None

    def set(self, pts, pts_color, boxes, boxes_color, texts):
        self.pts = pts
        self.pts_color = pts_color
        self.boxes = boxes
        self.boxes_color = boxes_color
        self.texts = texts

    def get(self):
        return {
            'pts': self.pts,
            'pts_color': self.pts_color,
            'boxes': self.boxes,
            'boxes_color': self.boxes_color,
            'texts': self.texts,
        }
