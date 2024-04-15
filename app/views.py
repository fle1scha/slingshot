# app/views.py
from flask import request, jsonify, render_template
from app import app, broadcaster

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        welcome_message = 'welcome! slingshot is a community adventure project. you\'ll hear from us soon.'
        success, error_message = broadcaster.send_message("", input_phone_number, welcome_message)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True, 'error_message': error_message}), 400
        
    return render_template('index.html')