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
AWS SNS

## Language
Python
