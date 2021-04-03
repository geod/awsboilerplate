# Startup Toolbag

## What is it?

A complete toolbag to get your idea live in minutes with a front to back architecture, infrastructure and pipeline.

Getting a new project is time consuming: Setting up the **front end web stack**
(which is a big enough problem in itself), building the **cloud infrastructure** (certificates, DNS, etc), **identity** integration, 
some form of **CICD pipeline** and **monitoring**. Putting **everything** together can be hours or days of configuration 
and integration. This is particularly true to add more production ready features - logging, monitoring, dev/prod or blue/green, 
robust and clean infrastructure.
 
The startup toolbag aims to integrate a number of technologies into a single project which enables you to get running in minutes.
It currently includes:
1. Front end web stack (leveraging the react boilerplate project)
2. Serverless application architecture back end (defined in CDK)
3. All infrastructure defined in code - certificates, route53, cloudfront, api-gateways (defined in CDK)
4. CICD pipeline which self-mutates, creates the infrastructure and builds/deploys the code on each commit

The novelty of the project is that all application, infrastructure, pipeline and monitoring are **fully* implemented in code in a single repo. 
Using the latest features in CDK - any commit which makes changes to any of this list (including the logic of the pipeline itself) will mutate and deploy.
This enables a single development experience where any element can be changed, committed and the pipeline will handle state changes.

![TUB Overview](documentation/TUB.jpg?raw=true "The Startup Toolbag")

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

## Background / Design Goals and Anti-Goals

### The Problem

As outlined above - the major problem is the time and complexity to integrate and assemble a fully featured development
and deployment architecture particularly when adding monitoring, logging, etc.

###  Serverless Archetype

The web archetype is very common and the [serverless variant](https://aws.amazon.com/lambda/resources/refarch/refarch-webapp/) 
is growing in popularity. It is difficult to estimate the % of overall projects that use this but it is safe to assume it is 
reasonably high and one of the most common architectures implemented.

![TUB Overview](documentation/RefArch_Serverless.png?raw=true "Serverless Reference Architecture")

### Options

There are a couple of different ways to build the serverless web application archetype

| Option | Pros | Cons |
| --- | --- | --- |
| 'PaaS Solution' <br> (Google App Engine, Heroku, Amplify, etc) | Great developer experience. Low startup costs. Requires only application developer skillset | Lower flexibility. Problems if you leave the fixed pattern. Can scale poorly in cost. |
| Cloud Native with Classic Tools: Terraform/Cloudformation | Full customization and flexibility | Significant setup cost and steep learning curve. Requires application and infrastructure skillset. May require coordinating infrastructure and application code
| Boilerplates | Great but  solve only one piece of the architecture | Work to assemble multiple components and integrate into a complete solution
| CDK Patterns Library | Great but each mini-pattern is only a fragment of the architecture | Work to assemble patterns together or integrate with front end solution
| AWS UI | Good to get going. Some work to assemble | Not repeatable. No leverage / effort each time |

### Enter - CDK & 'Infrastructure is Code'

[CDK](https://aws.amazon.com/blogs/developer/introducing-the-aws-cdk-public-roadmap/) was launched in 2019. The API has been
a work in progress for a while. CDK is still a bit 'rough' in places but it is rapidly getting better. However, the concept is powerful.
 
'Infrastructure as Code' is the most common term meaning  infra can be defined in declarative syntax. 
However, it is generally in specialized tools like Cloudformation or Terraform. It was generally not
fully integrated into the dev lifecycle, perhaps required a different skillset. Infrastructure (networks, servers, gateways, lambdas) still met application code somewhere in the middle. 
It was 'technically' code but did not gain the full advantage of software engineering concepts and practices. 
It is a half step where infrastructure folks could move 1/2 way to CICD, continuous push, etc.
1. Application Code -> Is Code
2. CICD Pipeline -> Yaml somewhere
3. Infrastructure -> Terraform
4. Monitoring -> Terraform, CLI or UI

IMO CDK need to more heavily push their 'Infastructure *is* code' [tagline](https://www.youtube.com/watch?v=ZWCvNFUN-sU) concept.
Once you get up to speed with CDK you gain the full advantage of software development practices (constructs, encapsulation, reuse, integration into the dev lifecycle)
in a *single repo/place* in a *single language* in a *single pipeline*. This makes development *really* fun again in a way that Cloudformation was not.

Furthermore, it offers the opportunity for *everything* to be in code in a single pipeline. 
I am not sure that the [self-mutating pipeline concept](https://docs.aws.amazon.com/cdk/api/latest/docs/pipelines-readme.html) is widely enough published. Once implemented everything *is* code:
1. Application Code -> Is Code (deployed by the pipeline)
2. CICD Pipeline -> Is Code (defined and self-mutates on commit)
3. Infrastructure -> Is Code (mutated by the pipeine)
4. Monitoring -> Is Code (mutated by the pipeine)

Put together it collapses what was previously distinct tools and lifecycles into a single language and pipeline.

### Design Goals and Anti-Goals

The design goals are
1. Provide quick set up of 'everything' required to get the basic front to back archetype 
2. Opinionated Jumping Off Point then Choose your own Adventure - Project provides a vanilla serverless archetype out the box. However,
developers will quickly find they need need to diverge/customize. The goal is to provide an opinionated starter kit then allow rapid divergence.
3. Feature Flag Patterns - The project currently has a feature flag to enable lambda serving from redis. It is disabled by default.
I am considering adding more sub-patterns with flags to enable/disable. This may be a trade-off between features for developers vs complexity/bloat to the overall project. 
4. Mini-PaaS - At one point I was toying with turning the project into a 'Native mini-PaaS' which would have included some form of Procfile ala Heroku. 
However, it seemed unnecessary and complex to build a wrapper that would ultimately generate CDK code. In effect, CDK starts to make AWS feel like a powerful 'native mini-PaaS'
5. CDK Patterns - Basic CDK comes with basic constructs - bucket, gateway, ec2, etc. Building a basic pattern like redirect from naked to www requires a bucket, cloudfront, route53.
This can be achieved in basic CDK but is tedious. CDK has started work on higher level constructs which are a software engineering abstraction to assemble low level constructs
into patterns. At the time of building not all the patterns were available. [HttpsRedirect](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_route53_patterns/README.html)
is used in the project. Over time it is anticipated that a lot of the code in the project could be compacted by using these pattern constructs.

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

