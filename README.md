# python-lambdas

A set of Lambda functions for processing our data using Python and libraries like `scikit-learn`. Uses [`chalice`](https://github.com/aws/chalice) for development and packaging.

## Setup

Ensure you are using Python@3.6, the latest Python version supported by AWS Lambda. We must install an older version via Brew to accomplish this:
```sh
$ brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
$ brew link python
```

Before activating any virtual environment, install `chalice` globally.
```sh
$ pip3 install chalice
```

In the root directory of this project,
```sh
$ python3 -m venv ./.env
$ source ./.env/bin/activate
$ pip3 install -r requirements.txt
```

## Running

```sh
$ chalice local --port=3100
```

## Deployment

Our current deployment process is a bit hacky, but suffices. Since our bundled app size exceeds Lambda's 50MB cap, we must use [a workaround](https://hackernoon.com/exploring-the-aws-lambda-deployment-limits-9a8384b0bec3) to deploy the app.

Ensure your credentials are setup correctly per [`chalice`'s instructions](https://github.com/aws/chalice#credentials).

In this project's root directory:
```sh
$ chalice package out
$ cd out
$ aws s3 cp ./ s3://test-lambda-deploys/ --recursive --exclude "*" --include "*.zip"
$ aws lambda update-function-code --function-name science-dev --region us-east-1 --s3-bucket test-lambda-deploys --s3-key deployment.zip
```
