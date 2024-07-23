import pymysql
from twilio.rest import Client
from config import Config
import sys

broadcast_text = "mailman again. please reply with your address. $40 on delivery.\n\nslingshot.wtf"

def validate_environment():
    """Validate the presence of required environment variables."""
    Config.validate()

def retrieve_contacts():
    """Retrieve unique phone numbers from Twilio messages."""
    twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    contacts = set()

    # Retrieve all phone numbers that have been sent messages
    messages = twilio_client.messages.list()
    for message in messages:
        # Check if the phone number is in the format +1XXXXXXXXXX
        if message.to.startswith('+1') and len(message.to) == 12:
            # Remove the leading +1 to get the 10-digit number
            phone_number = message.to[2:]
            contacts.add(phone_number)

    # print(f"Unique 10-digit phone numbers: {contacts}")
    print(f"Total number of unique 10-digit phone numbers: {len(contacts)}")
    print(contacts)
    return


def send_messages(contacts, target_number=None):
    """Send messages to the phone numbers using Twilio."""
    twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    failed_contacts = []

    if len(contacts) == 0 and target_number is None:
        print("No contacts in db and no target number provided. Cancelling text blast.")
        return

    if target_number:
        try:
            message = twilio_client.messages.create(
                from_=Config.TWILIO_PHONE_NUMBER,
                to=target_number,
                body=broadcast_text
            )
            print(f"Successfully initiated text blast to {target_number}. twilio sid: {message.sid}")
        except Exception as e:
            print(f"Failed to send text blast to {target_number}. twilio sid: {message.sid}")
            failed_contacts.append((None, target_number))
    else:
        for contact in contacts:
            if len(contact) == 2:
                _, phone_number = contact
            else:
                phone_number = contact
            try:
                message = twilio_client.messages.create(
                    from_=Config.TWILIO_PHONE_NUMBER,
                    to=phone_number,
                    body=broadcast_text
                )
                print(f"Successfully initiated text blast to {phone_number}. twilio sid: {message.sid}")
            except Exception as e:
                print(f"Failed to send text blast to {phone_number}. twilio sid: {message.sid}")
                failed_contacts.append((phone_number))

    return failed_contacts

def main():
    """Main function to execute the message broadcast process."""
    validate_environment()

    target_number = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "-n":
            if len(sys.argv) > 2:
                target_number = sys.argv[2]
            else:
                print("Error: No phone number provided with the -n parameter.")
                return
        elif sys.argv[1] == "-f":
            contacts = retrieve_contacts()
            return

    if target_number:
        failed_contacts = send_messages([], target_number)
    else:
        contracts = retrieve_contacts()
        print(contracts)
        # failed_contacts = send_messages(contacts)

    if failed_contacts:
        print(f"The following {len(failed_contacts)} contacts failed to receive the message:")
        for  phone_number in failed_contacts:
            print(f"Phone Number: {phone_number}")
        print("You can retry sending messages to the failed contacts.")

if __name__ == "__main__":
    main()