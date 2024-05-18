from flask import request, jsonify, render_template
from app import app, broadcaster

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        input_name = request.form['name']
        welcome_message = 'slingshot is a community adventure project.\n\nwe will text you about races, gatherings, and adventures.'
        success, error_message = broadcaster.send_message(input_name, input_phone_number, welcome_message)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': True, 'error_message': error_message}), 400
        
    return render_template('index.html')

@app.route('/cop', methods=['GET', 'POST'])
def cop_view():
    if request.method == 'POST':
        # Process the form data from the '/cop' route
        # You can add your custom logic here
        return jsonify({'success': True})
    
    return render_template('cop.html')