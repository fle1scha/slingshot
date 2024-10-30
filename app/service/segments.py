import requests

class SegmentService:
    def __init__(self, segments_repository):
        self.segments_repository = segments_repository

    def fetch_and_store_segment_times(self, access_token, athlete_data, segment_ids):
        """Fetch segment times for a given athlete and store them into the repository."""
        username = athlete_data['username']
        user_id = athlete_data['id']

        successful_inserts = []
        errors = []

        for segment_id in segment_ids:
            # Step: Check if the segment already exists for this athlete
            if self.segments_repository.check_segment_exists(user_id, segment_id):
                errors.append(f"Segment effort for user {username} and segment {segment_id} already exists. Skipping API call.")
                continue  # Skip this segment since it already exists

            try:
                # Fetch individual segment efforts using segment_id
                response = requests.get(
                f"https://www.strava.com/api/v3/segment_efforts",
                    params={
                        'segment_id': segment_id,
                        'start_date_local': '2024-01-01T00:00:00Z',
                        'end_date_local': '2024-10-30T00:00:00Z'
                    },
                    headers={'Authorization': f'Bearer {access_token}'}
                )

                # Debugging: Log the API call info
                print(f"Fetching segment efforts for Segment ID: {segment_id}")
                print(f"Response Status Code: {response.status_code}")

                if response.status_code == 200:
                    segment_data = response.json()
                    
                    # Debugging: Print the raw data received from API
                    print("Segment Data Retrieved:", segment_data)

                    # Updated parsing based on the actual response structure
                    if isinstance(segment_data, list):
                        for effort in segment_data:
                            # Parse the details from the effort
                            time_taken = effort.get('elapsed_time')  # Time in seconds
                            segment_name = effort['segment']['name']  # Use the segment name from effort
                            date_of_effort = effort['start_date']  # Date of the effort in ISO format

                            # Insert the segment time into the database
                            success, error = self.segments_repository.insert_segment_time(username, user_id, segment_id, time_taken, date_of_effort)
                            if success:
                                successful_inserts.append({
                                    'segment_name': segment_name,  # Segment name
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

        # Debugging: Log successful inserts and errors encountered
        print(f"Successful Inserts: {successful_inserts}")
        print(f"Errors Encountered: {errors}")

        return successful_inserts, errors

    def get_all_efforts_by_segment_ids(self, segment_ids):
        """Retrieve and format all segment efforts for specified segment IDs."""
        segment_efforts = {}

        for segment_id in segment_ids:
            efforts = self.segments_repository.get_all_times_by_segment_id(segment_id)
            
            if efforts:
                # Assume segment_id can be tied to a descriptive segment name (e.g., 'Climb', 'Sprint')
                segment_name = self._get_segment_name(segment_id)  # This should be a method that retrieves the segment name
                if segment_name not in segment_efforts:
                    segment_efforts[segment_name] = []

                for effort in efforts:
                    # Create a dictionary for each effort
                    segment_efforts[segment_name].append({
                        'username': effort['username'],
                        'user_id': effort['user_id'],
                        'time': effort['time_taken']
                    })

        # Optionally order the lists in each segment by time (ascending)
        for segment_name in segment_efforts:
            segment_efforts[segment_name].sort(key=lambda x: x['time'])  # Sort by time taken

        print(f"Segment Efforts: {segment_efforts}")  # Debugging output
        return segment_efforts

    def _get_segment_name(self, segment_id):
        """Retrieve segment name based on segment ID."""
        # Here you would implement logic to get the segment name from the database or a predefined list.
        # For example:
        segment_names = {
            17115468: "JDB's secret trail",
            792156: 'Strawberry Hill from incline start',
            9823103: 'Frisbee Golf CrossOver > JFK',
            1166988: 'Trail by the Aids Memorial Grove EB',
            627849: 'test: you should have run this',
        }
        return segment_names.get(segment_id, 'Unknown Segment')