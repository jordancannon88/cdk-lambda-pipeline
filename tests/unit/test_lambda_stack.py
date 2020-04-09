import json
import pytest

from aws_cdk import core
from pipeline.lambda_stack import LambdaStack


def get_template():
    app = core.App()
    LambdaStack(app, "LambdaStack")
    return json.dumps(app.synth().get_stack("LambdaStack").template)


def test_sqs_queue_created():
    assert ("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert ("AWS::SNS::Topic" in get_template())
