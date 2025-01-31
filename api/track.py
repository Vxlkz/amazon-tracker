import requests
from bs4 import BeautifulSoup
import json

def handler(event, context):
    body = json.loads(event['body'])
    tracking_number = body.get('tracking_number')

    if not tracking_number:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Tracking number is required'})
        }

    # Function to track the UPS package (can be modified for other carriers)
    def track_ups_package(tracking_number):
        url = f"https://www.ups.com/track?loc=en_US&tracknum={tracking_number}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            status = soup.find('div', class_="statusDetails")
            if status:
                return status.get_text(strip=True)
            else:
                return "Unable to find tracking status. Make sure the tracking number is correct."
        else:
            return "Failed to retrieve tracking information."

    # Get tracking status
    status = track_ups_package(tracking_number)

    # Return the status as JSON
    return {
        'statusCode': 200,
        'body': json.dumps({'status': status})
    }
