import json
import pytest

from aws_cdk import core
from will_dispatcher.will_dispatcher_stack import WillDispatcherStack


def get_template():
    app = core.App()
    WillDispatcherStack(app, "will-dispatcher")
    return json.dumps(app.synth().get_stack("will-dispatcher").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
