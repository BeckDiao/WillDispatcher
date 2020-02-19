import json
import boto3
import re
import smtplib
from email.message import EmailMessage

email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
table = boto3.resource('dynamodb').Table('living_test2')
ses = boto3.client('ses',region_name="us-west-2")

def lambda_handler(event, context):
    contact_list = get_contact_list()
    
    for email in contact_list.get('email'):
        send_email(email)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Send heartbeat check succeeded!')
    }

def get_contact_list():
    
    response = table.scan()
    
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    contact_list = {
        'sms': [],
        'email': []
    }
    
    for user_info in data:
        for contact in user_info.get("contact"):
            if re.search(email_regex, contact):
                contact_list.get('email').append(contact)
            else:
                contact_list.get('sms').append(contact)
        
    
    return contact_list

def send_email(recipient):
    print(recipient)
    SUBJECT = "Amazon SES Test (SDK for Python)"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Will Dispatcher Service Periodical Confirmation</h1>
      <p>Please send a "YES" to this email address.</p>
    </body>
    </html>
                """            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"

    response = ses.send_email(
        Destination={
            'ToAddresses': [
                recipient,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source="are.you.alive@willdispatcher.com"
    )
    
