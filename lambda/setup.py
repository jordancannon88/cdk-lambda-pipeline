import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="lambda-functions",
    version="0.0.1",

    description="A sample CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    install_requires=[
        "aws-cdk.core==1.31.0",
    ],

    python_requires=">=3.6",
)
