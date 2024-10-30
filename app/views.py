import requests
from flask import Flask, request, redirect, jsonify, session, render_template, url_for
from app import app, broadcaster, segments
from config import Config

app.secret_key = Config.FLASK_SECRET_KEY
REDIRECT_URI = Config.HOST+'/callback'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return handle_index_post(request)
    return render_template('index.html')

@app.route('/run', methods=['GET'])
def video():
    return render_template('sutropeaks.html')

@app.route('/register', methods=['GET'])
def strava():
    return render_template('strava.html')

@app.route('/login', methods=['GET'])
def login():
    authorization_url = (
        "https://www.strava.com/oauth/authorize"
        f"?client_id={Config.STRAVA_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=read,read_all"
    )
    return redirect(authorization_url)

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    access_token = exchange_code_for_token(code)
    
    if not access_token:
        return jsonify({'error': 'Failed to obtain access token from Strava'}), 400

    session['access_token'] = access_token
    return redirect(url_for('dashboard'))

def exchange_code_for_token(code):
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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('strava'))
    
    athlete_data = get_athlete_data(access_token)
    if not athlete_data:
        return jsonify({'error': 'Failed to fetch athlete data'}), 400

    segment_ids = [17115468, 792156, 9823103, 1166988, 627849]
    # 627849 - test
    # https://www.strava.com/segments/17115468
    # https://www.strava.com/segments/792156
    # https://www.strava.com/segments/9823103
    # https://www.strava.com/segments/1166988

    # Fetch and store segment times
    successful_inserts, errors = segments.fetch_and_store_segment_times(access_token, athlete_data, segment_ids)

    # Log after trying to fetch and store
    if errors:
        print(f"Errors Encountered: {errors}")
    else:
        print(f"Successful Inserts: {successful_inserts}")

    segment_efforts = segments.get_all_efforts_by_segment_ids(segment_ids)
    print(segment_efforts)
    return render_template('dashboard.html', athlete_data=athlete_data, segment_efforts=segment_efforts)

def handle_index_post(request):
    input_phone_number = request.form['phone_number']
    input_name = request.form['name']
    welcome_message = "www.slingshot.wtf/run <- tape from our last run, check it out! 10km trail run wednesday @ 18:30. bring a headlamp, make a friend. all paces, some prizes. we'll hold onto your stuff.\n\nstart and finish - google.com/maps?q=37.771,-122.4568."
    success, error_message = broadcaster.send_message(input_name, input_phone_number, welcome_message)

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': True, 'error_message': error_message}), 400
    
def get_athlete_data(access_token):
    """Fetch athlete data from Strava API."""
    response = requests.get("https://www.strava.com/api/v3/athlete", headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 200:
        return response.json()
    return None