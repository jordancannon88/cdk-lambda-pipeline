#!/usr/bin/env python3

from aws_cdk import core

from repo.codecommit_stack import CodeCommitStack
from pipeline.pipeline_stack import PipelineStack
from pipeline.lambda_stack import LambdaStack

app = core.App()

# [ CodeCommitStack ]
#
# The repository to hold this entire application.

CodeCommitStack(app, "CodeCommitStack")

# [ LambdaStack ]
#
# The Lambdas to be deployed that run the functions within the lambda folder.

lambda_stack = LambdaStack(app, "LambdaStack")

# [ PipelineDeployingLambdaStack ]
#
# A pipeline for pulling, testing, and building Lambdas.

PipelineStack(app, "PipelineDeployingLambdaStack",
              lambda_code=lambda_stack.lambda_code,
              env={'region': 'us-west-2'})

app.synth()
