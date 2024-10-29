from flask import Flask, request, redirect, jsonify, session, render_template, url_for
import requests
import os
from app import app, broadcaster, segments

# Set secret key for session management
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')  # Replace with your actual secret key

CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID', '138747')  # Store this in environment
CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET', '9c95b1af40fca98c823bbe3c2346715a64076061')  # Store this in environment
REDIRECT_URI = 'http://localhost:5000/callback'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        input_name = request.form['name']
        welcome_message = "www.slingshot.wtf/run <- tape from our last run, check it out! 10km trail run wednesday @ 18:30. bring a headlamp, make a friend. all paces, some prizes. we'll hold onto your stuff.\n\nstart and finish - google.com/maps?q=37.771,-122.4568."
        success, error_message = broadcaster.send_message(input_name, input_phone_number, welcome_message)

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True, 'error_message': error_message}), 400

    return render_template('index.html')

@app.route('/run', methods=['GET'])
def video():
    return render_template('sutropeaks.html')

@app.route('/strava')
def strava():
    return render_template('strava.html')

@app.route('/login')
def login():
    authorization_url = (
        "https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=read,read_all"
    )
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to obtain access token from Strava'}), 400

    data = response.json()
    access_token = data.get('access_token')
    session['access_token'] = access_token

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('strava'))

    response = requests.get("https://www.strava.com/api/v3/athlete", 
                             headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch athlete data'}), 400

    athlete_data = response.json()

    # Fetch and store segment times
    print(athlete_data)
    successful_inserts, errors = segments.fetch_and_store_segment_times(access_token, athlete_data)
    
    
     # Mock data for testing
    # Uncomment these lines to use mock data instead of fetching from the database for testing
    participants = [
        {'name': 'Alice', 'segment_time_1': '12:34', 'segment_time_2': '5:12', 'segment_time_3': '9:43'},
        {'name': 'Bob', 'segment_time_1': '11:20', 'segment_time_2': '4:50', 'segment_time_3': '8:15'},
        {'name': 'Charlie', 'segment_time_1': '13:07', 'segment_time_2': '6:02', 'segment_time_3': '10:25'},
    ]

    # Get all participants with segment times to display in the dashboard
    # participants = segments.get_all_segment_times()  # Fetch all participants and their segment times

    return render_template('dashboard.html', athlete_data=athlete_data, participants=participants)