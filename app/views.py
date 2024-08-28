from flask import request, jsonify, render_template
from app import app, broadcaster
from config import Config 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_phone_number = request.form['phone_number']
        input_name = request.form['name']
        welcome_message = 'slingshot is a community adventure project. we will text you soon.'
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
        admin_number = Config.ADMIN_PHONE_NUMBER

        order_message = f'slingshot.wtf order: {input_name}, {input_phone_number},  ordered a {input_size} {tshirt_type} shirt.'
        success_admin, error_message_admin = broadcaster.send_message(input_name, admin_number, order_message, False)

        if success_admin:
            order_success_message = f'mailman here. got your order for a {input_size} {tshirt_type} shirt. will be in touch about delivery.\n\nslingshot.wtf'

            success_user, error_message_user = broadcaster.send_message(input_name, input_phone_number, order_success_message, False)

            if success_user:
                return jsonify({'success': True})
            else:
                return jsonify({'error': True, 'error_message': error_message_user}), 400
        else:
            return jsonify({'error': True, 'error_message': error_message_admin}), 400
    
    return render_template('merch.html')