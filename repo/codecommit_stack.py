from aws_cdk import (
    core,
    aws_codecommit as cc,
)


class CodeCommitStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        commit = cc.Repository(self, 'CodeCommitRepo',
                               repository_name='LambdaTest',
                               description='LambdaTest repository'
                               )

        core.Tag.add(commit, "Creator", "Jordan")
