# WillDispatcher
A service used to automatically dispatch prewritten will to those people you love in case of death due to accident.

## High-level Idea:

### Sign Up/New User Setup
Tell the WillDispatcher service the following things:
1. The will. (currently, one will to all the people you list)
1. The list of contacts. Can be emails or Messages.
1. Monitor setting. (1) period to be asked (2) how many missing confirmation will trigger the dispatching.

### How the Service work
1. Periodically(like 1 day/week) ask users if they're still alive via Message or email.
1. If no confirmation is received from a specific user for continous multiple times(e.g. 3 continuous times), then WillDispatcher service would think that guy may have been dead.
1. Then WillDispatcher service will dispatch the will.

## Tools to be used
AWS Lambda Functions
DynamoDB
AWS S3
AWS CodePipeline
AWS SES(Simple Email Service)
AWS SNS

## Language
Python

## Components

### Heartbeat Lambda Function
1. Scan the `living` table and get the list of recipients.
1. Generate and send the emails.

### SES
Set the rule for receiving Emails. The received email will trigger database update lambda.

### Database Update Lambda Function
Update the `living` table with the received email.

### Check Lambda Function
1. Scan the living table to check if it's time to trigger the dispatch. <last_update + times_to_trigger + period>
1. If yes, send a message to SQS.

### SQS
Receive messages sent from **Check Lambda** and play a role as a trigger of **Dispatch Lambda**.

### Dispatch Lambda Function
1. Get the information from SQS and double check all the information is correct from DDB.
1. Get the will from S3.
1. Dispatch.


### Table for the dead
partition key: user id

```json
{
  "dead_beck": {
    "contact": "beck@gmail.com",
    "love_list": {
      "father": "father@gmail.com",
      "mother": "(+1)111-222-3333",
      "spouse": "spouse@gmail.com"
    },
    "will_position": "s3://bucket/key",
    "last_update": "123456789"
  }
}
```
### Table for the living
partition key: user id
sort key: period

```json
{
  "living_beck": {
    "period": "1 day",
    "contact": "beck@gmail.com",
    "times_to_trigger": 3,
    "love_list": {
      "father": "father@gmail.com",
      "mother": "(+1)111-222-3333",
      "spouse": "spouse@gmail.com'"
    },
    "will_position": "s3://bucket/key",
    "last_update": "123456789"
  }
}
```

## To do in the future
* Encryption towards will content.
* Security.
* Self-service signup system.
* Self-service will update.
