# cdk-lambda-codepipeline

A CI/CD pipeline with CodeCommit, CodeBuild, CodeDeploy, CodePipeline, and Lambda. The pipeline pulls, tests, builds, and deploys Lambdas using blue-green deployment and CDK.

## Lambda Function

All files pertaining to the python Lambda Function goes in the `lambda` folder.

Any required packages must be added into `setup.py` in the `lambda` folder. 

#### Required files
- requirements.txt
- setup.py

## Pipeline deploy

Deploy the CDK CodeCommit Stack:

```
$ cdk deploy CodeCommitStack
```

Upload this project in its entirety to the newly created repository.

Deploy the pipeline:

```
$ cdk deploy PipelineDeployingLambdaStack
```

The pipeline will be created and will pull from the CodeCommit repo and begin it's process before deploying the function within the `lambda` folder.

## CDK Python project instructions

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`ci_cd_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .env directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
