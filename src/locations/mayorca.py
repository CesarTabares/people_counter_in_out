from src.locations.base import LocationBase


class MayorcaLocation(LocationBase):
    VIDEO_URL = "../walking_people.mp4"
    MASK_P1 = LocationBase.Point(447, 150)
    MASK_P2 = LocationBase.Point(1080, 550)
    LIMITS_IN = [LocationBase.Point(447, 250), LocationBase.Point(1080, 250)]
    LIMITS_OUT = [LocationBase.Point(447, 445), LocationBase.Point(1080, 445)]

