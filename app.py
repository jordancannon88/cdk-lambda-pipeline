#!/usr/bin/env python3

from aws_cdk import core

from stacks.repo.codecommit_stack import CodeCommitStack
from stacks.pipeline.pipeline_stack import PipelineStack
from stacks.pipeline.lambda_stack import LambdaStack

app = core.App()

# [ CodeCommitStack ]
#
# The repository to hold this entire application.

repo_stack = CodeCommitStack(app, "CodeCommitStack")

# [ LambdaStack ]
#
# The Lambdas to be deployed that run the functions within the lambda folder.

lambda_stack = LambdaStack(app, "LambdaStack")

# [ PipelineDeployingLambdaStack ]
#
# A pipeline for pulling, testing, and building Lambdas.

pipeline_stack = PipelineStack(app, "PipelineDeployingLambdaStack",
                               lambda_code=lambda_stack.lambda_code)

# [ Tags ]
#
# Adds tags.

core.Tag.add(repo_stack, "Creator", "Jordan")
core.Tag.add(lambda_stack, "Creator", "Jordan")
core.Tag.add(pipeline_stack, "Creator", "Jordan")

app.synth()
