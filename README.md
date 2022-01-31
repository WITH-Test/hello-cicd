Real time status of the build: ![](https://codebuild.eu-west-3.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoid1d4WlJZeHlxa0s2TXdXeFUvc0d2LzlNODBQYzVtVGRGUUNTYk45YVVKRjVTNCs5M2pUSDNRTWk1MFdKY014bDhjUEdNbnJxU3E2TVc0OGtPcVhSL1p3PSIsIml2UGFyYW1ldGVyU3BlYyI6ImpVRHFKUlZweUhkdnVIZG4iLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)

# Setting up GitLab + CodeCommit

- create AWS Account under WITH organization: wow+aws@wadrid.com
- create GitLab account with email: wow+gitlab@wadrid.net
- create CodeCommit repo using root
- add IAM user to root: wow-aws-codecommit w/programmatic access and password (LastPass)
	* user permissions: AmazonCodeGuruReviewerFullAccess, AmazonCodeGuruProfilerFullAccess, AWSCodeCommitFullAccess
	* account ID arn:aws:iam::988760979462:user/wow-aws-codecommit

NOTE: it's best practice to leave users permissionless and add permissions using groups (i'll look into that)

## Setup ssh git credentials
push mirroring from GitLab to CodeCommit is broken

- login with IAM
- in GitLab: Repository > Settings > Mirroring repositories
	* add repo ssh address
	* detect host keys (accept host fingerprint)
	* copy public ssh key
	* https mirroring
- in AWS: IAM Console > Security credentials > AWS CodeCommit credentials 
	* paste the ssh key from GitLab

- configure GitLab with new ssh key : wow+gitlab@wadrid.net (LastPass)

## Setup https git credentials

- CC: generate git credentials for wow-aws-codecommit and download the generated .csv file
- in GitLab: Repository > Settings > Mirroring repositories
	* use the CC provided user: has `-at-` in the name
	* use the generated credentials to form the repo URL: https://<codecommit_user>@<repo_url>
	* use the password from the file
	* check `mirror only protected branches` (pushes faster)
	* accept

## Configuring AWS CI

- give full access permissions to `wow-aws-codecommit` to access CodeCommit, CodeBuild, CodePipeline, CodeGuru
	* there is a json policy with minimum privileges in [GL docs](https://docs.gitlab.com/ee/user/project/repository/mirror/push.html#set-up-a-push-mirror-from-gitlab-to-aws-codecommit)
- ~~ create a bucket (for artifacts?): ~~
- ~~ create a `buildspec.yml` at the root of the repo. this describes the build process (see example repo) ~~ We'll do this in the `buildspec.yml` editor
- create a new CodeBuild and CodePipeline with the correct info

# Creating Docker Images in the pipeline

## Setup AWS ECR (Registry)

- use the root account to create an ECR repository: wow-test
- add a policy for the AIM user to be able to push to the registry
	(JSON as soon as I find it again)


# Setting up a multi staged, cached, docker image build and ECR

See [Multi Stage](docs/multi_stage.md)
See [AWS CLI](docs/aws_cli.md)


CodeBuild: new build from CC repo, define buildspec in UI editor

`buildspec.yml`:

```yaml
version: 0.2

env:
    variables:
      CONTAINER_REPOSITORY_URL: 988760979462.dkr.ecr.eu-west-3.amazonaws.com/wow-test
      TAG_NAME: latest

phases:
  install:
    runtime-versions:
      docker: 19
  
  pre_build:
    commands:
    - $(aws ecr get-login --no-include-email)
    - docker pull $CONTAINER_REPOSITORY_URL:build-image || true
    - docker pull $CONTAINER_REPOSITORY_URL:$TAG_NAME || true
    
  build:
    commands:
    - docker build --target build-image --cache-from $CONTAINER_REPOSITORY_URL:build-image --tag $CONTAINER_REPOSITORY_URL:build-image .
    - docker build --target runtime-image --cache-from $CONTAINER_REPOSITORY_URL:build-image --cache-from $CONTAINER_REPOSITORY_URL:$TAG_NAME --tag $CONTAINER_REPOSITORY_URL:$TAG_NAME .

  post_build:
    commands:
    - docker push $CONTAINER_REPOSITORY_URL:build-image
    - docker push $CONTAINER_REPOSITORY_URL:$TAG_NAME
```

## CodePipeline

CodeBuild does not trigger builds automatically, it's only the configuration step. Pipelines do the wiring between CodeCommit and CodeBuild (and CodeDeploy later on).

# Getting the image

Using profile wowadmin (IAM administrator user)


```bash
$ export REGION=eu-west-3; export AWS_ACCOUNT_ID=988760979462; export ECR_REPO_NAME=wow-test
$ aws ecr get-login-password --region $REGION --profile wowadmin | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
$ docker pull $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${ECR_REPO_NAME}:latest
```
