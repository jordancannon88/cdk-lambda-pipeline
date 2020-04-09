import json

from aws_cdk import core
from stacks.pipeline.lambda_stack import LambdaStack


def get_template():
    app = core.App()
    LambdaStack(app, "LambdaStack")
    return json.dumps(app.synth().get_stack("LambdaStack").template)


def test_lambda_function_created():
    assert ("AWS::Lambda::Function" in get_template())
