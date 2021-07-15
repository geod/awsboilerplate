# Startup Toolbag

## What is it?

A complete boilerplate to get your idea live in minutes with a web front end, back end services, infrastructure, monitoring and CICD pipeline.

## Motivation

Getting a new project is time consuming: Setting up the front end web stack, back end services, 
cloud infrastructure (Certificates, DNS, API Gateways, etc), CICD pipeline (beta, prod or blue/green) and monitoring. 
Putting **everything** together can be hours or days of configuration and integration. Terraform is unsatisfying for most
developers and the console is not integrated into the development lifecycle.
 
The startup boilerplate aims to provide a full lambda web architecture and development experience to get you running in minutes. 
It currently includes:
1. Front end web stack (leveraging the react boilerplate project)
2. Serverless back end (request handling lambdas, background workers)
3. Infrastructure (certificates, route53, cloudfront, API Gateways
4. Monitoring (via cloudwatch)
5. CICD pipeline (deployment pipeline including beta, prod and self-mutation detailed below)

The novelty of the project is **all of the above elements** are implemented **in code**, in a **single mono repository**.
The project leverages CDK and some experimental features of CDK (CDKPipelines). Committing code changes to any element 
triggers the CICD pipeline which mutates the environment. 
We are calling this pattern 'Everything is Code' which is described in more detail below.

### Architecture Overview
The project implements a lambda reference architecture for web applications with CICD pipeline, building react front 
end for distribution via CloudFront over S3. An API Gateway fronts lambdas serving from S3 and a background worker.

![TUB Overview](documentation/TUB.jpg?raw=true "The Startup Toolbag")

### CICD Pipeline Process
A custom CICD pipeline leverages foundational features provided by [CDK Pipelines](https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/).
![TUB CICD](documentation/TUB-CICD%20Pipeline.jpg?raw=true "The Startup Toolbag CICD")

The pipeline allows the following workflows. Commiting changes to 
* application code (changing a lambda implementation) => pipeline will build and redeploy
* infrastructure (adding a lambda, adding an API gateway route) => pipeline will synthesize the cloudformation, compare to the current infrastructure and execute changes (add, modify, delete) to bring in line with the desired state
* pipeline definition (adding/deleting new stages to the pipeline logic) => one of the **first stages** of the pipeine is it will self-mutate to the new pipeline definition before running the rest of the pipeline

### Everything Is Code

Over the last decade infrastructure was moved into code. However, it is still partial in terms of covering all elements 
of the environment, change management and developer independence.

|**Infrastructure as Code** | 
|---|
|Scope is typically compute and networking|
|Tools targeted at the cloud or infrastructure team (Terraform). Steep learning curve or not accessible to developers |
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

The below gets you running without registering a domain name
1. Install the [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/cli.html)
2. Fork THEN clone this project (you have to fork vs clone as AWS will shortly attempt to pull and build it from github)
3. Create a python venv
```
virtualenv -p python3.8 .venv
pip install -r requirements.txt
```
4. Run `cdk bootstrap --trust <AWS ACCOUNT ID> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess` (this command sets up cdk on your account)
5. Optionally run `cdk synth` to test the tools are installed correctly
6. Log into github and create an access token to allow codepipeline to pull from the repository
7. Add this access token to AWS secrets manager using the following command
```
aws secretsmanager create-secret --name startuptoolbag-github-oath-token \
    --description "Start Up Toolkbag Git Auth Token" \
    --secret-string <YOUR OATH TOKEN>
```
8. Run `cdk deploy`. Note - setup is the *only* time you need to run cdk deploy to bootstrap the pipeline. 
On any future commits the pipeline will run and update the pipeline and infrastructure.
9. Log into codepipeline in your account and you will see a pipeline for the project. It should already be running
and will be building and deploying the infrastructure and code
10. Once the pipeline is complete you will be able to access the react front end

### Adding a domain name
You can also add a custom domain name for the project. The startuptoolbag supports all of the certificates,
cloud front distributions
1. Register a domain via Route53. It will automatically create a hosted zone
2. Run `aws route53 list-hosted-zones`. Take the hosted zone ID and domain name and enter them in `startuptoolbag_config.py`
```
hosted_zone_name = "<your domain name i.e. example.com>"
website_domain_name = "<Your Hosted Zone ID>"
```
3. Commit and push to your github fork. This will trigger the codepipeline build
4. Once the pipeline is complete you will be fully live

## Acknowledgements

In many ways the novelty of the project is to assemble and integrate multiple components into a full architecture/toolkit.

Acknowledgements
1. [react-boilerplate](https://github.com/react-boilerplate/react-boilerplate)

Other Reading
1. I found this too late into building startup-toolbag [CDK Patterns](https://cdkpatterns.com/)
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

