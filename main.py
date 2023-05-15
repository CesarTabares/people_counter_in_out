import argparse
from src.locations.factory import LocationFactory
from src.video_processor import VideoProcessor


def main(args):

    if not args.location:
        raise ValueError("Location name is required, pass it as --location <location_name>")

    factory = LocationFactory()
    location = factory.create_location(args.location)
    publisher = "Publisher()"
    video_processor = VideoProcessor(location, publisher, debug=args.debug)
    video_processor.start_stream_analysis()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', help='location name')
    parser.add_argument('--debug', help='debug mode')
    args = parser.parse_args()
    main(args)

