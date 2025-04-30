import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

account_sid = 'sid'
auth_token = 'token'
my_number = '+16195079194'
twilio_number = 'number'
twilio_client = Client(account_sid, auth_token)

# Constants
API_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/slot-availability'  # Replace with the actual URL
LOCATION_ID = 16547
#LOCATION_ID = 5101
CHECK_INTERVAL = 600  # Check every 10 minutes

# Function to alert the user
def send_sms_alert(message):
    try:
        message = twilio_client.messages.create(
            body=message,
            from_='twilio_number',  # Your Twilio phone number
            to='my_number'
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def format_available_slots(available_slots):
    formatted_slots = []
    for slot in available_slots:
        date = slot.get('startTimestamp', 'No date')
        formatted_slots.append(f"Date: {date}")
    
    return '\n'.join(formatted_slots)

# Function to check appointments
def check_appointments():
    response = requests.get(API_URL, params={
        'locationId': LOCATION_ID,
        'startDate': '2024-01-01',  # Adjust as needed
        'endDate': '2024-12-31'
    })

    if response.status_code == 200:
        data = response.json()
        available_slots = data.get('availableSlots', [])
        print(f"{available_slots}")
        
        if available_slots:  # Check if there are any available slots
            formatted_message = format_available_slots(available_slots)
            print(f"Appointments found:\n{formatted_message}")
            send_sms_alert(f"Global Entry Appointment Available!\n{formatted_message}\nhttps://ttp.cbp.dhs.gov/schedulerui")
        else:
            print("No appointments available.")
    else:
        print(f"API request failed with status code {response.status_code}")

if __name__ == "__main__":
    while True:
        check_appointments()
        time.sleep(CHECK_INTERVAL)