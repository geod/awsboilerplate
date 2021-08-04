<img src="https://raw.githubusercontent.com/geod/awsboilerplate/master/awsboilerplate/www/react-frontend/app/components/Header/banner.jpg" alt="awsboilerplate" align="center" />

<br />

## What is it?

Get live in minutes on aws with a react front end, back end lambdas, cloudfront and cicd pipeline.

## Motivation

When you have a new project or idea - you want to focus on the idea not configuration. The
 [serverless web application](https://aws.amazon.com/lambda/resources/refarch/refarch-webapp/) is a very popular pattern
  for building dynamic sites/applications. However, there remains **a lot** of setup to get this fully running: 
  cloudfront, s3 buckets, route53, certificates, API gateways, lambdas, 
code build and assembling a react/redux web stack and integrating it with codebuild, CICD, etc.  
 
Awsboilerplate provides a serverless web architecture **and** development experience that is deployable in a few commands.
It includes:
1. Front end react/redux stack (leveraging the react boilerplate project built via codebuild)
2. Lambda back end (including exemplars for common lambda patterns)
3. Infrastructure (certificates, route53, cloudfront, API Gateways)
4. Monitoring (via cloudwatch)
5. CICD pipeline (full CICD codepipeline and codebuild including self-mutation detailed below)

In addition to the above the project has two novel features:

Firstly, the project is fully implemented in [CDK](https://aws.amazon.com/cdk/). CDK is more developer friendly than CloudFormation or Terraform. 
The initial architecture is likely a good jumping off point for many developers. However, if you want to customize you have full access to change anything. It is an opinionated starter but open to adaptation.

The second feature is **every element** (front end, back end, cicd, infrastructure, monitoring) is implemented **in code**, in a **single mono repository**. 
It is possible to commit changes to any element and the pipeline will auto-magically mutate (this includes changes to the pipeline itself). This is made possible
by leverage one of the latest features in CDK called [CDKPipelines](https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/).
We are calling the pattern built ontop of CDK and CDKPipelines 'Everything is Code' which is described in more detail below.

### Architecture Overview
The project implements a lambda reference architecture for web applications with CICD pipeline, building react front 
end for distribution via CloudFront over S3. An API Gateway fronts lambdas serving from S3 and a background worker.

![Overview](documentation/AWS-Boilerplate-Architecture.jpg?raw=true "awsboilerplate")

### CICD Pipeline Process
A custom CICD pipeline combines CodePipline, Codebuild and [CDK Pipeline](https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/). 

![TUB CICD](documentation/AWS-Boilerplate-Pipeline.jpg?raw=true "awsboilerplate CICD")

The pipeline supports the following use-cases:
* Changing application code (changing the code behind a lambda) => Pipeline will deploy the new code
* Changing infrastructure (adding/delete constructs - S3/API Gw/Lamba/Certificates) => The CDK stage of the pipeline diffs the current vs requested state and automatically generates and executes the cloud formation changeset
![TUB CICD](documentation/AWS-Boilerplate-Infrastructure-Mutate.jpg?raw=true "Infrastructure Mutate")
* Changing the pipeline stages (adding/deleting new stages) => An early stage of the pipeline reads new version of the pipeline, rebootstraps to the new pipeline before continuing
![TUB CICD](documentation/AWS-Boilerplate-Pipeline-Mutate.jpg?raw=true "Pipeline Mutate")

### Everything Is Code

Every developer is likely familiar with the term 'Infrastructure as Code'. Over the last decade infrastructure has moved
from manual configuration to being implemented as code. However, it is still partial and does not cover all aspects of
a project or the developer experience ...

|**Infrastructure as Code** | 
|---|
|Scope limited to compute and networking resources|
|Tools target the cloud/infrastructure team (Terraform). Steep learning curve or not accessible to developers |
|Infrastructure definitions held in distinct repo from application code|
|Infrastructure changes made by the cloud/infrastructure team |
|Infrastructure deployed via CICD pipeline. Need for coordination with the application team|
|Infrastructure and Application skillset split across two teams |

The end state of this direction of travel is **everything is code**: all the elements get moved into code 
(application, infrastructure, monitoring, pipeline), change is consolidated and developers have more control.

|**Infrastructure as Code** | **Everything is Code**|
|---|---|
|Scope is typically compute and networking|Everything is defined in code (Application Code, Infrastructure, Pipeline, Monitoring) |
|Tools targeted at the cloud or infrastructure team (Terraform). Steep learning curve or not accessible to developers | Tools targeted at developers (CDK)|
|Infrastructure definitions held in distinct repo from application code| Definitions for everything held in single mono-repo|
|Infrastructure changes made by the cloud/infrastructure team | Everything accessible to developers |
|Infrastructure deployed by a distinct CICD pipeline. Application changes deployed by a different pipeline and coordination required | Singular pipeline handles all changes| 
|Infrastructure and Application skillset split across two teams | Developers more empowered with support from central cloud team |

## Prerequisites

1. Existing AWS Account
2. AWS CLI
3. Python / Pip / Virtualenv

## Quick Start 

### Register a domain name
1. Register a domain via Route53. It will automatically create a hosted zone
2. Run `aws route53 list-hosted-zones`. Take the hosted zone ID and domain name and enter them in `awsboilerplate_config.py`
```
hosted_zone_name = "<your domain name i.e. example.com>"
website_domain_name = "<Your Hosted Zone ID>"
```
3. Commit and push to your github fork. This will trigger the codepipeline build
4. Once the pipeline is complete you will be fully live

### Deploy awsboilerplate
1. Install the [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/cli.html)
2. Fork THEN clone this project (you need to fork as AWS will pull the code from github)
3. Create a python venv
```
virtualenv -p python3.8 .venv
pip install -r requirements.txt
```
4. Run `cdk bootstrap --trust <AWS ACCOUNT ID> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess` (this command sets up cdk on your account)
5. Run `cdk synth` to test the tools are installed correctly
6. Log into github and create an access token to allow codepipeline to pull from the repository
7. Add this access token to AWS secrets manager using the following command
```
aws secretsmanager create-secret --name awsboilerplate-github-oath-token \
    --description "awsboilerplate Git Auth Token" \
    --secret-string <YOUR OATH TOKEN>
```
8. Run `cdk deploy`. Note - setup is the *only* time you need to run cdk deploy to bootstrap the pipeline. 
On any future commits the pipeline will run and update the pipeline and infrastructure.
9. View codepipeline within the console. It should already be running
and will be building and deploying the infrastructure and code
10. Once the pipeline is complete you will be able to access the react from end using the domain address!

## Acknowledgements

In many ways the novelty of the project is to assemble and integrate multiple components into a full architecture/toolkit.

Acknowledgements
1. [react-boilerplate](https://github.com/react-boilerplate/react-boilerplate)
2. @rix0rrr provided invaluable help to answer a number of CDK questions

Other Reading
1. I found this too late into building awsboilerplate [CDK Patterns](https://cdkpatterns.com/)
2. Which is different from the official [AWS pattern library](https://github.com/aws-samples/aws-cdk-examples)

## Contributing

All contributions greatly appreciated. Trying to follow the edict from Reid Hoffman.
```
If you are not embarrassed by the first version of your product, you’ve launched too late
```
The launch version of the project is 'good enough' and solves many hours
of development time for people starting new project. 

There are many many features which could be added. Please submit a pull request.
Also see the features page for open features/issues.

## License

Copyright 2021 geod

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

