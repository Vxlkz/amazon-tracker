import requests
import json

def handler(event, context):
    body = json.loads(event['body'])
    tracking_number = body.get('tracking_number')

    if not tracking_number:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Tracking number is required'})
        }

    # Check if the tracking number starts with "TBA" (Amazon Logistics)
    def is_amazon_tracking_number(tracking_number):
        return tracking_number.startswith("TBA")

    # Function to generate Amazon tracking page URL
    def amazon_tracking_url(tracking_number):
        return f"https://www.amazon.com/gp/help/customer/display.html?nodeId=200465230&tracking_id={tracking_number}"

    # For Amazon packages (starting with TBA), we'll return the Amazon tracking URL
    if is_amazon_tracking_number(tracking_number):
        status = f"Track your package directly at Amazon: {amazon_tracking_url(tracking_number)}"
    else:
        status = "This tracking number is not recognized as an Amazon Logistics number."

    return {
        'statusCode': 200,
        'body': json.dumps({'status': status})
    }
