from aws_cdk import (
    core,
    aws_codecommit as codecommit,
)


class CodeCommitStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # [ CodeCommit: Repository ]
        #
        # Creates the repository to store the project in.

        commit = codecommit.Repository(self, 'CodeCommitRepo',
                                       repository_name='CodeCommitRepo',
                                       description='CodeCommitRepo repository'
                                       )

        # [ Tags ]
        #
        # Adds tags.

        # core.Tag.add(commit, "Creator", "Jordan")
