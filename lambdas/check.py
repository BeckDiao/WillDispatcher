import json
import boto3
import time

living_table = boto3.resource('dynamodb').Table('living_test2')
queue = boto3.resource('sqs').Queue('https://sqs.us-west-2.amazonaws.com/843135553029/test-queue')

def lambda_handler(event, context):
    
    # this lambda should be triggered every day
    # it will scan the whole living table:
    
    response = living_table.scan()
    
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = living_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        
    for user_info in data:
        """
        {'will_position': 's3://will-dispatcher-wills-storage-bucket/will_for_testing',
        'last_update': '1581223119', 
        'contact': ['beckdiao@gmail.com', 'xindiao11@qq.com'], 
        'user': 'living_beck', 
        'love_list': {'self': 'xindiao11@qq.com', 'spouse': 'rachelzhang114@gmail.com'},
        'period': '1 Day', 
        'times_to_trigger': Decimal('3'), 
        'remaining_times': Decimal('3')
        }
        """
        
        # for each item, do:
        # check if: current_timestamp - last_update -> days / period > times_to_trigger 
        # --> dispatch (send sqs message with "user")
        defined_period = user_info.get("period")
        delta = int((time.time() - int(user_info.get("last_update"))) / 60 / 60 / 24 / float(defined_period))
        
        if delta > user_info.get("times_to_trigger"):
            print("sending message")
            send_sqs_message(user_info.get("user"))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Periodical check is done!')
    }

def send_sqs_message(user_id):
    queue.send_message(MessageBody=user_id)

