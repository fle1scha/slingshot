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
            try:
                # Fetch individual segment efforts using segment_id
                response = requests.get(
                    f"https://www.strava.com/api/v3/segment_efforts",
                    params={
                        'segment_id': segment_id,
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

                    if isinstance(segment_data, list):
                        for effort in segment_data:
                            # Parse the details from the effort
                            time_taken = effort.get('elapsed_time')  # Time in seconds
                            date_of_effort = effort.get('start_date')  # Start date of the effort

                            # Insert the segment time into the database
                            success, error = self.segments_repository.insert_segment_time(username, user_id, segment_id, time_taken, date_of_effort)
                            if success:
                                successful_inserts.append({
                                    'segment_name': effort['segment']['name'],  # Segment name
                                    'time_taken': time_taken
                                })
                                print(f"Successfully inserted time for segment: {effort['segment']['name']}, Time Taken: {time_taken} seconds")
                            else:
                                if error == 'segment_exists':
                                    errors.append(f"Segment effort for user {username} and segment {segment_id} already exists.")
                                else:
                                    errors.append(f"Unknown error inserting segment time for user {username}: {error}")
                    else:
                        errors.append("Unexpected data format: Expected a list of segment efforts.")
                        print("Unexpected data format received from API.")

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
        results = []
        for segment_id in segment_ids:
            efforts = self.segments_repository.get_all_times_by_segment_id(segment_id)
            if efforts:
                results.extend(efforts)  # Combine results for each segment_id

        # Group results by username (athlete)
        athlete_results = {}
        for effort in results:
            username = effort['username']
            user_id = effort['user_id']
            segment_id = effort['segment_id']
            time_taken = effort['time_taken']

            if username not in athlete_results:
                athlete_results[username] = {
                    'user_id': user_id,
                    'times': {}
                }
            athlete_results[username]['times'][segment_id] = time_taken
        
        print(f"Athlete Results: {athlete_results}")  # Debugging output
        return athlete_results