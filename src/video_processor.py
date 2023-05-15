import math

import cv2
import numpy as np

from src.constants import YOLO_CLASS_NAMES
from src.libs.sort import Sort
from src.locations.base import LocationBase
from ultralytics import YOLO


class VideoProcessor:

    OBJECTS_OF_INTERESTS = ["person"]
    CONFIDENCE_LEVEL = 0.3

    def __init__(self, location: LocationBase, publisher, debug: bool = False):
        self.location = location
        self.publisher = publisher
        self.model = YOLO("yolo_model/weights/yolov8m.pt")
        self.tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
        self.debug = debug
        self.objects_data = {}
        self.counted_ids = []
        self.count_in = 0
        self.count_out = 0

    def start_stream_analysis(self):
        video_capture = self.location.get_video_capture()

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            self.location.build_mask()
            frame_region = self.get_frame_region(frame)
            results = self.model(frame_region, stream=True, device="mps", verbose=False)
            detections = self.add_detections(results)
            results_tracker = self.tracker.update(dets=detections)
            self.process_detected_objects(frame, results_tracker)

            if self.debug:
                self.show_and_draw_frame_limits(frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break

        video_capture.release()
        cv2.destroyAllWindows()

    def get_frame_region(self, frame):
        frame_region = cv2.bitwise_and(frame, frame, mask=self.location.mask)
        return frame_region

    @staticmethod
    def add_detections(results):
        detections = np.empty((0, 5))
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(lambda n: int(n), box.xyxy[0])
                conf = math.ceil(box.conf[0] * 100) / 100
                cls = int(box.cls[0])
                current_class = YOLO_CLASS_NAMES[cls]
                if current_class in VideoProcessor.OBJECTS_OF_INTERESTS and conf > VideoProcessor.CONFIDENCE_LEVEL:
                    current_array = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, current_array))

        return detections

    def process_detected_objects(self, frame, results_tracker):
        for result in results_tracker:
            x1, y1, x2, y2, id_ = map(lambda n: int(n), result)
            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            if id_ not in self.counted_ids:
                object_data = self.set_object_data(id_, cy)
                self.decide_object_count(object_data, cx, cy)

                if self.debug:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    cv2.putText(frame, f'{id_}-{object_data.get("direction")}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 0, 0), 2)

    def set_object_data(self, id_: int, cy: int):
        object_data = self.objects_data.get(id_)
        if not object_data:
            object_data = {
                "id_": id_,
                "init_cy": cy,
                "direction": None,
                "counted": False,
            }
            self.objects_data.update({id_: object_data})
        else:
            if object_data.get("direction") is None:
                if cy - object_data.get("init_cy") >= 2:
                    object_data.update({"direction": "out"})
                elif cy - object_data["init_cy"] <= -2:
                    object_data.update({"direction": "in"})

        return object_data

    def decide_object_count(self, object_data: dict, cx, cy):
        object_data_direction = object_data.get("direction")
        id_ = object_data.get("id_")

        if object_data_direction == "in":
            if self.location.LIMITS_IN[0].x < cx < self.location.LIMITS_IN[1].x and self.location.LIMITS_IN[0].y - 15 < cy < self.location.LIMITS_IN[1].y + 15:
                self.count_in += 1
                self.counted_ids.append(id_)
                del self.objects_data[id_]
        elif object_data_direction == "out":
            if self.location.LIMITS_OUT[0].x < cx < self.location.LIMITS_OUT[1].x and self.location.LIMITS_OUT[0].y - 15 < cy < self.location.LIMITS_OUT[1].y + 15:
                self.count_out += 1
                self.counted_ids.append(id_)
                del self.objects_data[id_]

    def show_and_draw_frame_limits(self, frame):
        cv2.rectangle(frame, (self.location.MASK_P1.x, self.location.MASK_P1.y), (self.location.MASK_P2.x, self.location.MASK_P2.y), (255, 0, 255), thickness=2)
        cv2.line(frame, (self.location.LIMITS_IN[0].x, self.location.LIMITS_IN[0].y), (self.location.LIMITS_IN[1].x, self.location.LIMITS_IN[1].y), (0, 255, 0), thickness=2)
        cv2.line(frame, (self.location.LIMITS_OUT[0].x, self.location.LIMITS_OUT[0].y), (self.location.LIMITS_OUT[1].x, self.location.LIMITS_OUT[1].y), (0, 0, 255), thickness=2)
        cv2.putText(frame, f"IN: {self.count_in}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(frame, f"OUT: {self.count_out}", (100, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.imshow(self.location.__class__.__name__, frame)
