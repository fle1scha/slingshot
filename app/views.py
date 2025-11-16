import requests
from flask import Flask, request, redirect, jsonify, session, render_template, url_for
from config import Config
from app import app, broadcaster, strava, arena, limiter

app.secret_key = Config.FLASK_SECRET_KEY
REDIRECT_URI = Config.HOST + '/callback'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@limiter.limit("5 per minute")  
def handle_index_post():
    input_phone_number = request.form.get('phone_number')
    input_name = request.form.get('name')

    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'unknown')

    app.logger.info(f"POST from {client_ip} | UA: {user_agent} | Name: {input_name} | Phone: {input_phone_number}")
    
    welcome_message = (
        "slingshot is a community adventure project. we'll text you soon. STOP to opt out."
    )

    success, error_message = broadcaster.send_welcome_message(
        input_name, input_phone_number, welcome_message
    )

    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': True, 'error_message': error_message}), 400
 
@app.route('/login', methods=['GET'])
def login():
    authorization_url = strava.get_authorization_url()
    return redirect(authorization_url)

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    access_token = strava.exchange_code_for_token(code)
    
    if not access_token:
        return jsonify({'error': 'Failed to obtain access token from Strava'}), 400

    session['access_token'] = access_token
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))  # Redirect to the login route, not 'strava'

    athlete_data = strava.get_athlete_data(access_token)
    if not athlete_data:
        return jsonify({'error': 'Failed to fetch athlete data'}), 400

    # Fetch and store segment times via the strava service
    successful_inserts, errors = strava.fetch_and_store_segment_data(access_token, athlete_data)

    # Get segment efforts via the strava service
    segment_efforts = strava.get_segment_efforts()

    print(segment_efforts)
    
    return render_template('dashboard.html', athlete_data=athlete_data, segment_efforts=segment_efforts)

@app.route('/api/arenadata', methods=['GET'])
def get_are_na_images():
    """API endpoint to get images from Are.na"""
    images = arena.fetch_images()
    return jsonify(images)
