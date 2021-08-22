<img src="https://raw.githubusercontent.com/geod/awsboilerplate/master/awsboilerplate/www/app/components/Header/banner.jpg" alt="awsboilerplate" align="center" />

<br />

## What is it?

Get live in minutes on aws with a react front end, back end lambdas, cloudfront and CICD pipeline.

## Motivation

When you have a new project or idea - you want to focus on the idea not setup. The
 [serverless web application](https://aws.amazon.com/lambda/resources/refarch/refarch-webapp/) is a very popular pattern
  for building dynamic sites/applications. However, there remains **a lot** of setup to get this fully running: 
  cloudfront, s3 buckets, route53, certificates, API gateways, lambdas, CORS, assembling a react/redux web stack, integrating it with codebuild, CICD, etc. 
  This setup can take hours or days depending on experience and the sophistication of the setup. The console approach is not repeatable and cloudformation/terraform have a steep learning curve and are not developer friendly.
 
Awsboilerplate provides a serverless web architecture **and** development experience that is fully deployable in a few commands.
It includes:
1. Front end react/redux stack (leveraging the react boilerplate project built via codebuild)
2. Lambda back end (including exemplars for common lambda patterns)
3. Infrastructure (certificates, route53, cloudfront, API Gateways)
4. Monitoring (via cloudwatch)
5. CICD pipeline (full CICD codepipeline and codebuild including self-mutation detailed below)
6. The front end and lambdas can be developed/iterated locally using SAM (setup also included)

In addition to the above the project has two novel features:

Firstly, the project is fully implemented in [CDK](https://aws.amazon.com/cdk/). CDK allows the entire infrastructure to be expressed in code. CDK is more developer friendly than CloudFormation or Terraform. 

The second feature is **every element** (front end, back end, cicd, infrastructure, monitoring) is implemented **in code**, in a **single mono repository**. 
It is possible to commit changes to any element and the pipeline will auto-magically mutate (this includes changes to the pipeline itself). This is made possible
by leverage one of the latest features in CDK called [CDKPipelines](https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/).
We are calling the pattern built ontop of CDK and CDKPipelines 'Everything is Code' which is described in more detail below.

The initial architecture is likely a good jumping off point for many developers. If you want to customize and build on it you have full access to change anything. It is an opinionated starter but open to adaptation.

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

## Running AWS Boilerplate

### Local Quickstart & Development
AWSBoilerplate can be run locally.

1. Fork and checkout the project
2. `cd awsboilerplate/app/lambda_hello_world; sam local start-api`
3. `cd awsboilerplate/www; npm start`
4. Open http://localhost:3000/

### Deploy to AWS
1. Fork THEN clone this project (you need to fork as AWS will pull the code from github)
2. Create a python venv
```
virtualenv -p python3.8 .venv
pip install -r requirements.txt
```
3. Install [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/cli.html). Run `cdk synth` to test the tools are installed correctly
4. Run `cdk bootstrap --trust <AWS ACCOUNT ID> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess` (this command sets up cdk on your account) 
5. Log into github and create an access token to allow codepipeline to pull from the repository
6. Add this access token to AWS secrets manager using the following command
```
aws secretsmanager create-secret --name awsboilerplate-github-oath-token \
    --description "awsboilerplate Git Auth Token" \
    --region us-east-1
    --secret-string <YOUR OATH TOKEN>
```
7. Register a domain via Route53 which will create a hosted zone. Run `aws route53 list-hosted-zones`. Take the hosted zone ID and domain name and enter them in `awsboilerplate_config.py`
```
hosted_zone_name = "<your domain name i.e. example.com>"
website_domain_name = "<Your Hosted Zone ID>"
```

8. Update the server URL in `awsboilerplate/www/internals/webpack/webpack.prod.babel.js`
```
    new webpack.EnvironmentPlugin({
      SERVER_URL: 'https://api.<Your domain name>' // <-- Keep https://api prefix. An API Gateway will be created for this URL
    }),
``` 

9. Commit and push (to your github fork)
10. Run `cdk deploy`. CDK will create the pipeline defined in `awsboilerplate/pipeline/cdk_pipeline_stack.py`. 
When this pipeline runs it will create all of the infrastructure defined in `awsboilerplate/infra and app`.

### Development Cycle / Making Changes

You can develop features locally changing **both** the front end and the lambdas. This includes changing, adding or deleting new lambdas

When ready to push simply run
```buildoutcfg
-- usual git add, git commit --
git push origin master
```

The cdkpipeline will pick up the changes to both the application code and infrastructure and mutate both. Once the
pipeline runs you can hit the domain name to see the new changes (remember cloudfront cache may be enabled).

## Comparison to Alternatives

| Option | Ease of Getting Started / Learning Curve | Developer Experience | Flexibility* | Cost |
|---|---|---|---|---|
| awsboilerplate (cdk/aws native) | Easy |  Okay | High | Low |
| Codepipeline or Jenkins etc ontop of Terraform / Cloudformation | Difficult | Poor | High | Low |
| Heroku | Super Easy | Superb | Moderate | High |
| Porter | Easy | Good | Low/Moderate | Low |

\* Ability when your app becomes complex or your use-case doesn't quite fit to customize.

## Roadmap

1. Integration with cognito to have a full user account setup
2. Currently you can run locally or after registering a domain. I believe it is possible to run it without creating a domain.
It would involve additional complexity of somehow passing the API gateway address to React (it creates a dependency 
between the dynamic infrastructure creation stage and react).
3. It is very easy to add beta then prod (potentially add more sophisticated rolling deployment)

## Limitations

### Experience with CDK
CDK is great / clearly the future. It is very close to being a super powerful developer experience. Given it is still relatively new
(and CDKPipeline is very new) there are a few issues I encountered:

1. Even for a simple archetype like `awsboilerplate` the pipeline time is between 10-20 minutes. Even if infrastructure changes are not being made
CDK is very slow to synthesize and confirm that no changes have been made. When infrastructure changes are made then 
it can significantly increase pipeline time. This made it painfully slow to build the initial stages of the project (particularly when I was making a lot of mistakes).
CDKPipeline seems to have fewer cache and performance speed ups in comparison to regular Codepipeline. I hope that AWS can make this faster over time
because if they could get the pipeline time down to <10 minutes it would be a fabulous development experience.
2. Current CDK is not really designed to accommodate the 'everything is code' pattern that this project has created. 
It assumes that application artifacts have been built prior to CDK running. CDK is then able to 'deploy' those artifacts when
lambdas or buckets are created. The goal of awsboilerplate was to have a **single** pipeine for everything. As a result,
we have pushed the boundaries of the CDKPipeline API. (and is the reason why `cdk_pipeline_stack.py` uses both 
standard codepipeline and cdkpipelines). There is a whole blog article but I had to run through 6-7 major different design changes to the current design.
3. I did want *all* changes to be self-mutating. Because of the limitations above any changes to the reactbuild which are run before
the pipeline mutates are not self-mutating. As a result changing the react build requires a `cdk deploy`
4. CDK under the covers still gets translated into cloudformation. It can still be a bit 'delicate' and sometimes major
refactoring of infrastructure can fail to execute and I generally deleted and recreated the entire stack.

### Other
1. The AWS native devops tools - codebuild and codepipeline could be way better. A combination of cryptic error messages (example: if you create a codepipeline and the secret it relies on is not created it just fails to create. 
No description / error message hinting at why). Simple builds are all 5-10 minutes. They are difficult to debug given limited access (I often created debug statement in the buildspec but each run is 5-10 minutes)


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

