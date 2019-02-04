import json
import os
import boto3
from dotenv import load_dotenv
from lambda_decorators import load_json_body, cors_headers

load_dotenv()

SOURCE = os.getenv("SOURCE")
DESTINATION = os.getenv("DESTINATION")
SUBJECT = os.getenv("SUBJECT")
ORIGIN = os.getenv("ORIGIN")

@cors_headers(origin=ORIGIN)
@load_json_body
def mailer(event, context):

    client = boto3.client('ses')
    data = event['body']

    name = data['name']
    email = data['email']
    message = data['message']
    phone = data['phone']

    _message = "Message from: " + name + "\nEmail: " + \
        email + "\nMessage content: " + message + "\nPhone: " + \
        phone

    email_response = client.send_email(
        Destination={
            'ToAddresses': [DESTINATION]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': _message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': SUBJECT,
            },
        },
        Source=SOURCE,
    )

    response = {
        "statusCode": 200,
        "body": json.dumps(email_response)
    }

    return response