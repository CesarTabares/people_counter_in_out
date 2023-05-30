from src.locations.base import LocationBase


class MayorcaLocation(LocationBase):
    VIDEO_URL = "http://2.tcp.ngrok.io:13642/stream"
    MASK_P1 = LocationBase.Point(24, 51)
    MASK_P2 = LocationBase.Point(770, 561)
    LIMITS_IN = [LocationBase.Point(24, 151), LocationBase.Point(760, 151)]
    LIMITS_OUT = [LocationBase.Point(24, 461), LocationBase.Point(760, 461)]


# class MayorcaLocation(LocationBase):
#     VIDEO_URL = "../walking_people.mp4"
#     MASK_P1 = LocationBase.Point(447, 150)
#     MASK_P2 = LocationBase.Point(1080, 550)
#     LIMITS_IN = [LocationBase.Point(447, 250), LocationBase.Point(1080, 250)]
#     LIMITS_OUT = [LocationBase.Point(447, 445), LocationBase.Point(1080, 445)]

