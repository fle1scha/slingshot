import requests
from config import Config

class ArenaService:
    def __init__(self, channel_slug='left-coast'):
        """Initialize with the channel slug."""
        self.api_url = f'http://api.are.na/v2/channels/{channel_slug}/contents?per=10'

    def fetch_images(self):
        """Fetch images from the Are.na channel."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            # Filter out the contents that are images
            images = [
                item['image']['display'] for item in data['contents'] if 'image' in item
            ]   
            print(images)
            return images
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Are.na data: {e}")
            return []
