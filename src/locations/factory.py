from src.locations.mayorca import MayorcaLocation


class LocationFactory:

    @staticmethod
    def create_location(location_name):
        if location_name.lower() == "mayorca":
            return MayorcaLocation()
        else:
            raise ValueError("Unknown location")