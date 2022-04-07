# GitHub Actions

Limitations of the free version:
- Organization-wide templates and actions are not available for private repos in free version.
- 500 min/month of Actions (triggers for self-hosted runners are free)

## First things first

Created an Organization: [WITH-Test](https://github.com/WITH-Test)

## How do GitHub Actions work?

Create a base public repo, `.github`, for the Organization:
- here we'll have `workflow-templates`, to give easy access and configuration to projects

Everything is handled in separate repositories, that can make use of each other.

Testing [this](https://github.com/MartinHeinz/workflows/blob/v1.0.0/.github/workflows/python-container-ci.yml) from the article [here](https://dev.to/martinheinz/ultimate-ci-pipeline-for-all-of-your-python-projects-2ob8)

## Connecting AWS and GitHub

We need to configure AWS to trust GitHub in order to push container images to the ECR repo.
I did this manually, but I found an [AWS CDK example](https://github.com/dannysteenman/aws-cdk-examples/tree/main/openid-connect-github) that might be worth trying if we need to configure this again.

## Create AWS Resources

Configuring AWS for each repo and each branch is going to be a pain in the butt to do by hand.
The same repo from above has an example of TS CDK stack to create all these resources. Checking it out.
