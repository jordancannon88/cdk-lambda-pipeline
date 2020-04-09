from aws_cdk import core, aws_codedeploy as codedeploy, aws_lambda as lambda_

from datetime import datetime


class LambdaStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs):
        super().__init__(app, id, **kwargs)

        # [ Lambda: Code ]
        #
        # This represents the code to be supplied by the pipeline.

        self.lambda_code = lambda_.Code.from_cfn_parameters()

        # [ Lambda: Function ]
        #
        # Creates the Lambda.

        func = lambda_.Function(self, "Lambda",
                                code=self.lambda_code,
                                handler="index.handler",
                                runtime=lambda_.Runtime.PYTHON_3_7,
                                )

        # [ Lambda: Version ]
        #
        # Adds versions to the Lambda with date of code execution.

        version = func.add_version(datetime.now().isoformat())

        # [ Lambda: Alias ]
        #
        # Adds aliasing to the Lambda to allow for blue-green deployment.

        alias = lambda_.Alias(self, "LambdaAlias",
                              alias_name="Prod", version=version)

        # [ CodeDeploy: Deployment Group ]
        #
        # Creates the group for Lambda(s) for the Aliases.

        codedeploy.LambdaDeploymentGroup(self, "DeploymentGroup",
                                         alias=alias,
                                         deployment_config=
                                         codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
                                         )
