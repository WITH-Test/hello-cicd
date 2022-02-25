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


CodeBuild: new build from CC repo, define [buildspec.yml](docs/buildspec.yml) in UI editor

Making sure to put the right name in the last command, that will put a file in the S3, pointing to the image that was just pushed.

## CodePipeline

CodeBuild does not trigger builds automatically, it's only the configuration step. Pipelines do the wiring between CodeCommit and CodeBuild (and CodeDeploy later on).

# Getting the image

Using profile wowadmin (IAM administrator user)

```bash
$ export REGION=eu-west-3; export AWS_ACCOUNT_ID=988760979462; export ECR_REPO_NAME=wow-test
$ aws ecr get-login-password --region $REGION --profile wowadmin | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
$ docker pull $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${ECR_REPO_NAME}:latest
$ docker run -p 8000:8000 $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/${ECR_REPO_NAME}:latest  # runs on port 8000
```

## CodeDeploy to AWS Fargate

~~Let's try to run the image in EC2 Spot instances after the build.~~

(Note: Fargate does the managing of the instances. Spot instances are to be managed manually in the EC2 section. I think)

Resources:
[Spot EC2 + Lambda + CW Events](https://aws.amazon.com/blogs/devops/automatic-deployment-to-new-amazon-ec2-on-demand-and-spot-instances-using-aws-codedeploy-amazon-cloudwatch-events-and-aws-lambda/) (seems outdated)

[Create ECS Cluster](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-ec2-cluster-console-v2.html)

[Create ECS Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-service-console-v2.html)

For the task running on the VPC to be able to pull the image we just published, we need to give it permissions, with a role. See [tutorial](https://docs.aws.amazon.com/codepipeline/latest/userguide/ecs-cd-pipeline.html).

# Accessing the new application over the internet

[Create a LB and Target Group](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/tutorial-application-load-balancer-cli.html):

```bash
$ aws --profile wowadmin elbv2 create-load-balancer --name wow-very-balanced --subnets subnet-<zone-3a> subnet-<zone-3b> --security-groups sg-<vpc-group>
$ aws --profile wowadmin elbv2 create-target-group --name wow-hello-aws-target --protocol HTTP --port 80 --vpc-id vpc-<vpcId> --ip-address-type ipv4
```

That returned [this](docs/lb_create.json) and [this](docs/tg_create.json).


https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/

## Restart the wizard

I was getting lost in all of the above, since it wasn't working. I restarted from scratch, setting all options as defaults 
and setting the target to `FARGATE`. Updated `buildspec.yml` to force a redeploy of the task. 
I needed to add a [new policy to update the ECS service](https://docs.aws.amazon.com/AmazonECS/latest/userguide/security_iam_id-based-policy-examples.html)
to the `CodeBuildDockerCacheRole` role.
