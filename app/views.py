from flask import request, jsonify, render_template
from app import app, broadcaster
from config import Config 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        input_name = request.form['name']
        welcome_message = "slingshot is a community adventure project. bike 'race'; 27/09, 18:00; location & format next week. off-road bikes encouraged, but never enforced.\n\nreply MORPH to receive updates for this event."
        success, error_message = broadcaster.send_message(input_name, input_phone_number, welcome_message)

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True, 'error_message': error_message}), 400

    return render_template('index.html')

@app.route('/video', methods=['GET'])
def video():
    return render_template('video.html')