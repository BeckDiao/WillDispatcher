from aws_cdk import (
    aws_events as events,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_events_targets as targets,
    core
)


class WillDispatcherStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # IAM roles for

        # Lambda functions
        heartbeat_lambda = _lambda.Function(
            self, 'HeartbeatLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='heartbeat.lambda_handler',
        )
        heartbeat_rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )
        heartbeat_rule.add_target(heartbeat_lambda)
        # rule.add_target(targets.LambdaFunction(heartbeat_lambda))

        update_lambda = _lambda.Function(
            self, 'UpdateDDBLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='update.lambda_handler',
        )

        check_lambda = _lambda.Function(
            self, 'PeriodicalCheckLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='check.lambda_handler',
        )
        check_rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )
        check_rule.add_target(check_lambda)

        dispatch_lambda = _lambda.Function(
            self, 'DispatchLambda',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='dispatch.lambda_handler',
        )

        # SQS
        queue = sqs.Queue(
            self, "WillDispatcherQueue",
            visibility_timeout=core.Duration.seconds(300),
        )

