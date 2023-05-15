import argparse
from src.locations.factory import LocationFactory
from src.video_processor import VideoProcessor


def main(location_name: str):

    if not location_name:
        raise ValueError("Location name is required, pass it as --location <location_name>")

    factory = LocationFactory()
    location = factory.create_location(location_name)
    publisher = "Publisher()"
    video_processor = VideoProcessor(location, publisher)
    video_processor.start_stream_analysis()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', help='location name')
    args = parser.parse_args()
    location_name = args.location
    main(location_name)

