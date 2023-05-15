from src.locations.factory import LocationFactory
from src.video_processor import VideoProcessor

if __name__ == "__main__":
    factory = LocationFactory()
    location = factory.create_location("mayorca")
    publisher = "Publisher()"
    video_processor = VideoProcessor(location, publisher)
    video_processor.start_stream_analysis()
