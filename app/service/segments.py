import requests
from datetime import datetime, timezone

class SegmentService:
    def __init__(self, segments_repository):
        self.segments_repository = segments_repository

    def fetch_and_store_segment_times(self, access_token, athlete_data, segment_ids):
        """Fetch segment times for a given athlete and store them into the repository."""
        user_id = athlete_data['id']
        successful_inserts = []
        errors = []

        for segment_id in segment_ids:
            try:
                # Fetch individual segment efforts using segment_id
                response = requests.get(
                    f"https://www.strava.com/api/v3/segment_efforts",
                    params={
                        'segment_id': segment_id,
                        'start_date_local': '2024-10-29T00:00:00Z',
                        'end_date_local': '2024-10-31T00:00:00Z'
                    },
                    headers={'Authorization': f'Bearer {access_token}'}
                )


                if response.status_code == 200:
                    segment_data = response.json()
                    
                    # Debugging: Print the raw data received from API

                    if isinstance(segment_data, list):
                        for effort in segment_data:
                            time_taken = effort.get('elapsed_time')  # Time in seconds
                            segment_name = effort['segment']['name']
                            date_of_effort = effort['start_date']  # Date of the effort in ISO format
                            
                            # Get username from athlete_data or from segment_data if None
                            username = athlete_data['username'] if athlete_data['username'] is not None else athlete_data['firstname']

                            success, error = self.segments_repository.insert_segment_time(username, user_id, segment_id, time_taken, date_of_effort)
                            if success:
                                successful_inserts.append({
                                    'segment_name': segment_name,
                                    'time_taken': time_taken
                                })
                                print(f"Successfully inserted time for segment: {segment_name}, Time Taken: {time_taken} seconds")
                            else:
                                errors.append(f"Unknown error inserting segment time for user {username}: {error}")
                    else:
                        errors.append("Unexpected data format: Expected a list of segment efforts.")
                        print("Unexpected data format received from API: Expected a list but received:", segment_data)
                else:
                    errors.append(f"Failed to fetch data for segment ID {segment_id}: {response.status_code}")

            except requests.HTTPError as e:
                errors.append(f"HTTP error fetching segment {segment_id}: {str(e)}")
            except Exception as e:
                errors.append(f"General error fetching segment {segment_id}: {str(e)}")

        print(f"Successful Inserts: {successful_inserts}")
        print(f"Errors Encountered: {errors}")

        return successful_inserts, errors

    def get_all_efforts_by_segment_ids(self, segment_ids, filter_date=None):
        """Retrieve and format all segment efforts for specified segment IDs filtered by date."""
        segment_efforts = {}

        # Default to today if no date is provided
        if filter_date is None:
            filter_date = datetime.now(timezone.utc).date()
        else:
            # Ensure filter_date is a date object from string if necessary
            if isinstance(filter_date, str):
                filter_date = datetime.fromisoformat(filter_date).date()

        for segment_id in segment_ids:
            efforts = self.segments_repository.get_all_times_by_segment_id(segment_id, filter_date)
            print(f"Efforts for Segment ID {segment_id}: {efforts}")  # Debugging output

            if efforts:
                segment_name = self._get_segment_name(segment_id)
                if segment_name not in segment_efforts:
                    segment_efforts[segment_name] = []

                # Directly append the relevant efforts
                for effort in efforts:
                    segment_efforts[segment_name].append({
                        'username': effort['username'],
                        'user_id': effort['user_id'],
                        'time': effort['time_taken']
                    })

        # Optionally order the lists in each segment by time (ascending)
        for segment_name in segment_efforts:
            segment_efforts[segment_name].sort(key=lambda x: x['time'])  # Sort by time taken

        return segment_efforts

    def _get_segment_name(self, segment_id):
        """Retrieve segment name based on segment ID."""
        segment_names = {
            17115468: "JDB",
            792156: 'Strawberry Hill',
            9823103: 'Frisbee Golf CrossOver',
            1166988: 'Aids Memorial Grove'        
        }
        return segment_names.get(segment_id, 'Unknown Segment')