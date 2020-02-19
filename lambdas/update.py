import json
import boto3
import time

contact_to_user_table = boto3.resource('dynamodb').Table('contact_to_user')
living_table = boto3.resource('dynamodb').Table('living_test2')

def lambda_handler(event, context):
    # get email from event/context
    email_address = event.get("Records")[0].get("ses").get("mail").get("source")
    
    # get user id from table `contact_to_user`
    response = contact_to_user_table.get_item(
        Key={'contact': email_address}
    )
    user = response.get('Item').get('user')
    
    # get times_to_trigger before updating
    living_response = living_table.get_item(
        Key={'user': user}
    )
    times_to_trigger = living_response.get("Item").get("times_to_trigger")
    
    # update living table
    # TODO: update the last_update
    living_table.update_item(
        Key={'user': user},
        UpdateExpression="set last_update = :r",
        ExpressionAttributeValues={
            ':r': int(time.time()),
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Update living table for {user} successfully!')
    }

