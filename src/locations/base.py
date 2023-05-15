from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Any
import cv2
import numpy as np


class LocationBase(ABC):

    Point = namedtuple('Point', ('x', 'y'))
    VIDEO_URL: str
    MASK_P1: Point
    MASK_P2: Point
    LIMITS_IN: list[Point, Point]
    LIMITS_OUT: list[Point, Point]

    def __init__(self):
        self.video_width = 0
        self.video_height = 0
        self.mask = None
        self.directions = {}
        self.count_in = 0
        self.count_out = 0

    @classmethod
    def __init_subclass__(cls, **kwargs):
        required_properties = ['VIDEO_URL', 'MASK_P1', 'MASK_P2', 'LIMITS_IN', 'LIMITS_OUT']
        for prop in required_properties:
            if not hasattr(cls, prop):
                raise TypeError(f"property '{prop}' is not defined in class {cls.__name__}.")
        super().__init_subclass__(**kwargs)

    def get_video_capture(self):
        capture = cv2.VideoCapture(self.__class__.VIDEO_URL)
        self.video_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return capture

    def build_mask(self):
        self.mask = np.zeros((self.video_height, self.video_width), dtype=np.uint8)
        cv2.rectangle(
            self.mask,
            (self.__class__.MASK_P1.x, self.__class__.MASK_P1.y),
            (self.__class__.MASK_P2.x, self.__class__.MASK_P2.y),
            (255, 255, 255),
            -1
        )



