<img src="https://raw.githubusercontent.com/geod/awsboilerplate/master/awsboilerplate/www/app/components/Header/banner.jpg" alt="awsboilerplate" align="center" />

<br />

## What is it?

Get live in minutes with a complete stack: react front end, lambdas, infrastructure and CICD pipeline.

## Motivation

Everyone wants to focus on the idea and not setup / config fiddling. The
 [serverless web application](https://aws.amazon.com/lambda/resources/refarch/refarch-webapp/) is a common pattern for building web applications / startups.
 However, there is often hours or days of setup to create a **complete** and robust setup.
 
Awsboilerplate is a complete and integrated boilerplate including:
1. Front end react/redux stack (leveraging the react boilerplate project built via codebuild)
2. Lambda back end (including exemplars for common lambda patterns)
3. Infrastructure (certificates, route53 domains and DNS setup, cloudfront, API Gateways)
4. Monitoring
5. CICD pipeline (including self-mutation detailed below)
6. React and the lambdas can be developed locally before deployment (setup also included)

All the build, config and wiring is complete. Everything is defined in CDK and is [self-mutating](documentation/everything_is_code.md)

[Live Demo](https://www.awsboilerplate.io/) contains a front end calling a 'hello world' lambda.

## Prerequisites

1. Existing AWS Account
2. AWS CLI
3. Python / Pip / Virtualenv

## Quickstart

### Run Locally
AWSBoilerplate can be run locally.

1. Fork and checkout the project
2. `cd awsboilerplate/app/lambda_hello_world; sam local start-api`
3. `cd awsboilerplate/www; npm start`
4. Open http://localhost:3000/

### Run on AWS
1. Fork THEN clone this project (you need to fork as AWS will pull the code from your github project)
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

### Architecture Overview
The project implements a lambda reference architecture for web applications with CICD pipeline, building react front 
end for distribution via CloudFront over S3. 

![Overview](documentation/AWS-Boilerplate-Architecture.jpg?raw=true "awsboilerplate")

### 'Everything is Code'

awsboilerplate has a few novel features.

The project leverages [CDK](https://aws.amazon.com/cdk/). CDK allows the entire infrastructure to be expressed in code and is relatively developer friendly. 

Furthermore, awsboilerplate leverages one of the latest features within CDK - [CDKPipelines](https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/).

The project leverages these two technologies and wires them into a pattern where:

> 1. Every element (front end, back end, cicd, infrastructure, monitoring) is implemented **in code**, in a **single mono repository**.
> 2. It is possible to commit a change to any element and the pipeline should auto-magically make it happen (including changes to the pipeline itself) 

We are calling this pattern 'Everything is Code' which is further detailed [here](documentation/everything_is_code.md)

## Documentation

1. ['Everything is Code'](documentation/everything_is_code.md)
2. [Alternatives](documentation/alternatives.md)
3. [Roadmap](documentation/roadmap.md)
4. [Limitations](documentation/limitations.md)

## Acknowledgements

awsboilerplate assemble and integrates multiple technologies into a full architecture/toolkit. The only novelty is
stretching CDK to support a single mono-repository and combined pipeline.

Acknowledgements
1. [react-boilerplate](https://github.com/react-boilerplate/react-boilerplate) is just fabulous
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

