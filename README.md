# Startup Toolbag

## What is it?

A complete toolbag to get your idea live in minutes with a front to back architecture, infrastructure and CICD pipeline - all expressed in code.

## Motivation

Getting a new project is time consuming: Setting up the **front end web stack**
(which is a big enough problem in itself), building the **cloud infrastructure** (certificates, DNS, etc), **identity** integration, 
some form of **CICD pipeline** and **monitoring**. Putting **everything** together can be hours or days of configuration 
and integration. This is particularly true to add more production ready features - logging, monitoring, dev/prod or blue/green, 
robust and clean infrastructure.
 
The startup toolbag integrates a number of technologies to enable you to get running in minutes with a smooth development experience on a robust infrastructure. It currently includes:
1. Front end web stack (leveraging the react boilerplate project)
2. Serverless back end (leveraging AWS lambda)
3. Infrastructure (certificates, route53, cloudfront, api-gateways)
4. CICD pipeline (self mutates and deploys all infrastructure and application code)

The novelty of the project is all application, infrastructure, pipeline and monitoring are **fully** implemented in code. 
1. Application code => python
2. Infrastructure => Defined in code (CDK)
3. Monitoring => Defined in code (CDK)
4. CICD Pipeline => Defined in code (CDK Pipeline, Code Pipeline and Codebuild)
A commit which makes changes to **any of this list** will **be automatically deployed by the pipeline** (including the logic of the pipeline itself). 

### Architecture Overview
![TUB Overview](documentation/TUB.jpg?raw=true "The Startup Toolbag")

### CICD Pipeline Process
![TUB CICD](documentation/TUB-CICD%20Pipeline.jpg?raw=true "The Startup Toolbag CICD")

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
4. Run `cdk bootstrap` (this command sets up cdk on your account)
5. Optionally run `cdk synth` to test the tools are installed correctly
6. Log into github and create an access token to allow codepipeline to pull from the repository
7. Add this access token to AWS secrets manager using the following command
```
aws secretsmanager create-secret --name startuptoolbag-github-oath-token \
    --description "Start Up Toolkbag Git Auth Token" \
    --secret-string <YOUR OATH TOKEN>
```
8. Run `cdk deploy`. Note - setup is the *only* time you need to run cdk deploy
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

