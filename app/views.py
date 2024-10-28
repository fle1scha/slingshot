from flask import request, jsonify, render_template
from app import app, broadcaster
from config import Config 

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
