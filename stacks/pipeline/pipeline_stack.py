from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_lambda as lambda_,
                     aws_s3 as s3,
                     aws_events as event)


class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *,
                 lambda_code: lambda_.CfnParametersCode = None,
                 sns_target, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # [ CodeCommit: Repository ]
        #
        # Grabs the repository the pipeline will be pulling from.

        code = codecommit.Repository.from_repository_name(self, "ImportedRepo",
                                                          "CodeCommitRepo")

        # [ CodeBuild: Project: CDK ]
        #
        # Creates the project for building the Lambda CloudFormation template using CDK.

        cdk_build = codebuild.PipelineProject(self, "CdkBuild",
                                              build_spec=codebuild.BuildSpec.from_object(dict(
                                                  version="0.2",
                                                  phases=dict(
                                                      install=dict(
                                                          commands=[
                                                              "npm install -g aws-cdk",
                                                              "cdk --version",
                                                              "python --version",
                                                              "pip install -r requirements.txt"
                                                          ]),
                                                      pre_build=dict(
                                                          commands=[
                                                              "python -m pytest tests"
                                                          ]
                                                      ),
                                                      build=dict(commands=[
                                                          "cdk synth -o dist"
                                                      ])),
                                                  artifacts={
                                                      "base-directory": "dist",
                                                      "files": [
                                                          "LambdaStack.template.json"]},
                                                  environment=dict(buildImage=
                                                                   codebuild.LinuxBuildImage.STANDARD_2_0))))

        # [ CodeBuild: Project: Lambda ]
        #
        # Creates the project for building the Lambda Functions.

        lambda_build = codebuild.PipelineProject(self, 'LambdaBuild',
                                                 build_spec=codebuild.BuildSpec.from_object(dict(
                                                     version="0.2",
                                                     phases=dict(
                                                         install=dict(
                                                             commands=[
                                                                 "cd lambda",
                                                                 "pip install -r requirements.txt"
                                                             ]
                                                         ),
                                                         post_build=dict(
                                                             commands=[
                                                                 "pytest"
                                                             ]
                                                         )
                                                     ),
                                                     artifacts={
                                                         "base-directory": "lambda",
                                                         "files": [
                                                             "index.py"]},
                                                     environment=dict(buildImage=
                                                                      codebuild.LinuxBuildImage.STANDARD_2_0))))

        # [ CodePipeline: Artifacts ]
        #
        # Creates the artifacts.

        source_output = codepipeline.Artifact()
        cdk_build_output = codepipeline.Artifact("CdkBuildOutput")
        lambda_build_output = codepipeline.Artifact("LambdaBuildOutput")

        # [ S3: Location ]

        lambda_location = lambda_build_output.s3_location

        # [ CodePipeline: Stages: Actions ]
        #
        # Creates the pipeline stages actions.

        repo_source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit_Source",
            repository=code,
            output=source_output)

        lambda_build_action = codepipeline_actions.CodeBuildAction(
            action_name="Lambda_Build",
            project=lambda_build,
            input=source_output,
            outputs=[lambda_build_output])

        cdk_build_action = codepipeline_actions.CodeBuildAction(
            action_name="CDK_Build",
            project=cdk_build,
            input=source_output,
            outputs=[cdk_build_output])

        cdk_deploy_action = codepipeline_actions.CloudFormationCreateUpdateStackAction(
            action_name="Lambda_CFN_Deploy",
            template_path=cdk_build_output.at_path(
                "LambdaStack.template.json"),
            stack_name="LambdaDeploymentStack",
            admin_permissions=True,
            parameter_overrides=dict(
                lambda_code.assign(
                    bucket_name=lambda_location.bucket_name,
                    object_key=lambda_location.object_key,
                    object_version=lambda_location.object_version)),
            extra_inputs=[
                lambda_build_output])

        # [ CodePipeline ]
        #
        # Creates the pipelines.

        pipeline = codepipeline.Pipeline(self, "Pipeline",
                                         stages=[
                                             codepipeline.StageProps(stage_name="Source",
                                                                     actions=[
                                                                         repo_source_action]),
                                             codepipeline.StageProps(stage_name="Build",
                                                                     actions=[
                                                                         lambda_build_action,
                                                                         cdk_build_action]),
                                             codepipeline.StageProps(stage_name="Deploy",
                                                                     actions=[
                                                                         cdk_deploy_action])
                                         ]
                                         )

        # [ CodePipeline: Events ]
        #
        # Creates the events for the pipeline, stages, and actions.

        repo_source_action.on_state_change('RepoSourceStateChange',
                                           target=sns_target,
                                           event_pattern=event.EventPattern(
                                               detail={'state': [
                                                   'FAILED'
                                               ]}))

        lambda_build_action.on_state_change('LambdaBuildStateChange',
                                            target=sns_target,
                                            event_pattern=event.EventPattern(
                                                detail={'state': [
                                                    'FAILED'
                                                ]}))

        cdk_build_action.on_state_change('CDKBuildStateChange',
                                         target=sns_target,
                                         event_pattern=event.EventPattern(
                                             detail={'state': [
                                                 'FAILED'
                                             ]}))

        cdk_deploy_action.on_state_change('CDKDeployStateChange',
                                          target=sns_target,
                                          event_pattern=event.EventPattern(
                                              detail={'state': [
                                                  'FAILED'
                                              ]}))

        pipeline.on_state_change('PipelineStateChange',
                                 target=sns_target,
                                 event_pattern=event.EventPattern(
                                     detail={'state': [
                                         'SUCCEEDED'
                                     ]}))
