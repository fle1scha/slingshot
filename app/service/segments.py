import requests

class SegmentService:
    def __init__(self, segments_repository):
        self.segments_repository = segments_repository

    def fetch_and_store_segment_times(self, access_token, athlete_data):
        """Fetch segment times for a given athlete and store them into the repository."""

        username = athlete_data['username']

        if self.segments_repository.check_user_exists(username):
            return "User already exists in the database.", []

        successful_inserts = []
        errors = []
        segment_ids = [123456, 654321, 987654]  # Replace with your actual segment IDs
        
        for segment_id in segment_ids:
            try:
                response = requests.get(
                    f"https://www.strava.com/api/v3/segments/{segment_id}/all_efforts",
                    headers={'Authorization': f'Bearer {access_token}'}
                )

                if response.status_code == 200:
                    segment_data = response.json()
                    for effort in segment_data['all_athlete_efforts']:
                        time_taken = effort['elapsed_time']  # Time in seconds
                        segment_name = segment_data['name']  # Segment name

                        # Insert the segment time into the database
                        self.segments_repository.insert_segment_time(athlete_data['id'], segment_name, time_taken)
                        successful_inserts.append({
                            'segment_name': segment_name,
                            'time_taken': time_taken
                        })
                else:
                    errors.append(f"Failed to fetch data for segment ID {segment_id}: {response.status_code}")
            
            except requests.HTTPError as e:
                errors.append(f"Error fetching segment {segment_id}: {str(e)}")
            except Exception as e:
                errors.append(str(e))

        return successful_inserts, errors

    def get_all_segment_times(self):
        """Retrieve all segment times for all participants."""
        return self.segments_repository.get_all_segments()  # This call is indirect and uses the repository method