import json
import boto3
import smtplib
from email.message import EmailMessage

living_table = boto3.resource('dynamodb').Table('living_test2')
dead_table = boto3.resource('dynamodb').Table('dead-test')
s3 = boto3.resource('s3')
ses = boto3.client('ses', region_name="us-west-2")


def lambda_handler(event, context):
    user_id = event["Records"][0]["body"]

    # Get info from living table
    # needed info: user(str), love_list(map), contact(list), will_position(str)
    living_response_items = living_table.get_item(Key={'user': user_id}).get("Item")
    love_list = living_response_items.get("love_list")
    will_position = living_response_items.get("will_position")
    contact = living_response_items.get("contact")

    # get content of will from will_position
    obj = s3.Object("will-dispatcher-wills-storage-bucket", will_position)
    will_body = obj.get()['Body'].read()

    # Move the item from living table to dead table
    dead_table_response = dead_table.put_item(
        Item={
            'user': user_id,
            'love_list': love_list,
            'contact': contact,
            'will_position': will_position
        }
    )
    living_table.delete_item(Key={"user": user_id})

    # dispatch - send emails to each one in love_list
    for relationship, email in love_list.items():
        send_email(email, user_id, will_body, relationship)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def send_email(recipient, user, content, relationship):
    print(recipient)
    SUBJECT = f"{user} loves you but failed to speak out"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (f"Hi, you should be the {relationship} of {user}. The following is {user} 's will: {content}")

    # The HTML body of the email.
    # BODY_HTML = """<html>
    # <head></head>
    # <body>
    #   <h1>Will Dispatcher Service is dispatching</h1>
    # </body>
    # </html>
    #             """            

    BODY_HTML = f"<html><body> Hi, you should be the {relationship} of {user}. The following is {user} 's will: {content}</body></html>"

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
        Source="they.love.you@willdispatcher.com"
    )
