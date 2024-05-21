from flask import request, jsonify, render_template
from app import app, broadcaster
from config import Config  # Ensure that my_number is properly stored in your config

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

@app.route('/merch', methods=['GET', 'POST'])
def merch_view():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        input_name = request.form['name']
        input_size = request.form['shirt_size']
        tshirt_type = request.form['tshirt_type']
        admin_number = Config.ADMIN_PHONE_NUMBER  # Ensure that admin_number is properly stored in your config

        # Message to be sent to 'admin_number'
        order_message = f'slingshot.wtf order: {input_name}, {input_phone_number},  ordered a {input_size} {tshirt_type} shirt.'
        success_admin, error_message_admin = broadcaster.send_message(input_name, admin_number, order_message, False)

        if success_admin:
            # Message to be sent to the user
            order_success_message = f'mailman here. got your order for a {input_size} {tshirt_type} shirt. will be in touch about delivery.\n\nslingshot.wtf'

            success_user, error_message_user = broadcaster.send_message(input_name, input_phone_number, order_success_message, False)

            if success_user:
                return jsonify({'success': True})
            else:
                # Return error if user message fails
                return jsonify({'error': True, 'error_message': error_message_user}), 400
        else:
            # Return error if admin message fails
            return jsonify({'error': True, 'error_message': error_message_admin}), 400
    
    return render_template('merch.html')