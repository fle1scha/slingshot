import requests

def send_phone_numbers(phone_numbers):
    url = "http://slingshotwtf-env-1.eba-q45z42ip.us-east-2.elasticbeanstalk.com/"
    name = "anon"

    for phone_number in phone_numbers:
        data = {
            "name": name,
            "phone_number": phone_number
        }
        
        response = requests.post(url, data=data)
        
        # Checking the response status
        if response.status_code == 200:
            print(f"Successfully sent phone number: {phone_number}")
        else:
            print(f"Failed to send phone number: {phone_number}")
            print(f"Response text: {response.text}")

# Example list of phone numbers

# Send the phone numbers
send_phone_numbers(phone_numbers)