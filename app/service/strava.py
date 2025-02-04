import requests
from config import Config

class StravaService:
    def __init__(self, segment_service, segment_ids=None, event_date=None):
        """Initialize with optional segment_ids, event_date, and SegmentService."""
        self.segment_service = segment_service  # Accept the segment_service as an argument
        self.segment_ids = segment_ids or [26592018, 1750852, 968449, 996627]
        self.event_date = event_date or "2024-11-14"

    def get_authorization_url(self):
        """Generate the authorization URL for Strava OAuth."""
        return (
            "https://www.strava.com/oauth/authorize"
            f"?client_id={Config.STRAVA_CLIENT_ID}"
            "&response_type=code"
            f"&redirect_uri={Config.HOST}/callback"
            "&scope=read,read_all"
        )

    def exchange_code_for_token(self, code):
        """Exchange the authorization code for an access token."""
        token_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': Config.STRAVA_CLIENT_ID,
            'client_secret': Config.STRAVA_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=payload)

        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        return None

    def get_athlete_data(self, access_token):
        """Fetch and return the athlete's data from Strava."""
        athlete_url = "https://www.strava.com/api/v3/athlete"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(athlete_url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Returns the athlete's data
        return None  # Returns None if the request fails or if the athlete's data is unavailable

    def fetch_and_store_segment_data(self, access_token, athlete_data):
        """Fetch and store segment times, and return the results."""
        successful_inserts, errors = self.segment_service.fetch_and_store_segment_times(
            access_token, athlete_data, self.segment_ids
        )

        if errors:
            print(f"Errors Encountered: {errors}")
        else:
            print(f"Successful Inserts: {successful_inserts}")

        return successful_inserts, errors

    def get_segment_efforts(self):
        """Retrieve segment efforts based on segment IDs."""
        return self.segment_service.get_all_efforts_by_segment_ids(self.segment_ids, self.event_date)
