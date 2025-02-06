import requests
import random

class ArenaService:
    def __init__(self, channel_slug='left-coast'):
        """Initialize with the channel slug."""
        self.channel_slug = channel_slug

    def fetch_images(self):
        """Fetch images from the Are.na channel with a random page number."""
        page_number = random.randint(1, 5)  # Adjust range as needed
        api_url = f'http://api.are.na/v2/channels/{self.channel_slug}/contents?per=7&page={page_number}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            # Filter out the contents that are images
            images = [
                item['image']['display'] for item in data.get('contents', []) if 'image' in item
            ]   
            print(images)
            return images
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Are.na data: {e}")
            return []
