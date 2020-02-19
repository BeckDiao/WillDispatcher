#!/usr/bin/env python3

from aws_cdk import core

from will_dispatcher.will_dispatcher_stack import WillDispatcherStack


app = core.App()
WillDispatcherStack(app, "will-dispatcher", env={'region': 'us-west-2'})

app.synth()
