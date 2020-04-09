import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk-lambda-pipeline",
    version="0.0.1",

    description="A CodePipeline for building, testing, and releasing Lambda functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Jordan Cannon",

    package_dir={"": "lambda"},
    packages=setuptools.find_packages(where="lambda"),

    install_requires=[
        "aws-cdk.core==1.31.0",
        "aws-cdk.aws_iam==1.31.0",
        "aws-cdk.aws_codecommit==1.31.0",
        "aws-cdk.aws_codebuild==1.31.0",
        "aws-cdk.aws_codedeploy==1.31.0",
        "aws-cdk.aws_lambda==1.31.0",
        "aws-cdk.aws_codepipeline==1.31.0",
        "aws-cdk.aws_codepipeline_actions==1.31.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
