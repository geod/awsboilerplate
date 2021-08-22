## Everything Is Code
The awsboilerplate project leverages CDK. What this means is 'everything' is defined in code in a single mono repository

1. Application code (react and lambdas) => defined in code (see `awsboilerplate/app` and `awsboilerplate/www`)
2. Infrastructure (Cloudfront, Certificates, API Gateways, S3, etc) => defined in code (see `awsboilerplate/infra`)
2. CICD Pipeline => defined in code (see `awsboilerplate/pipeline`)

The project then builds upon one of the latest features of CDK - CDK Pipelines. A custom pipeline
has been wired together.

The pipeline supports the following use-cases:
* Changing application code (changing the code behind a lambda) => Pipeline will deploy the new code
* Changing infrastructure (adding/delete constructs - S3/API Gw/Lamba/Certificates) => The CDK stage of the pipeline diffs the current vs requested state and automatically generates and executes the cloud formation changeset
* Changing the pipeline stages (adding/deleting new stages) => An early stage of the pipeline reads new version of the pipeline, rebootstraps to the new pipeline before continuing

##### UC-1: App Code Push
![TUB CICD](AWS-Boilerplate-Pipeline.jpg?raw=true "awsboilerplate CICD")

##### UC-1: Infra Code Push (delete a lambda)
![TUB CICD](AWS-Boilerplate-Infrastructure-Mutate.jpg?raw=true "Infrastructure Mutate")

##### UC-1: Pipeline Change Push
![TUB CICD](AWS-Boilerplate-Pipeline-Mutate.jpg?raw=true "Pipeline Mutate")

## Defining: Everything Is Code

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

The end state of this direction of travel is **everything is code** which we are defining with three elements:
1. all the elements get moved into code (application, infrastructure, monitoring, pipeline)
2. change is consolidated (no bifurcated infrastructure and application pipeline, coordination or change control)
3. developers are the primary users (change is consolidate in developers vs spread across development and operations team)

|**Infrastructure as Code** | **Everything is Code**|
|---|---|
|Scope is typically compute and networking|Everything is defined in code (Application Code, Infrastructure, Pipeline, Monitoring) |
|Tools targeted at the cloud or infrastructure team (Terraform). Steep learning curve or not accessible to developers | Tools targeted at developers (CDK)|
|Infrastructure definitions held in distinct repo from application code| Definitions for everything held in single mono-repo|
|Infrastructure changes made by the cloud/infrastructure team | Everything accessible to developers |
|Infrastructure deployed by a distinct CICD pipeline. Application changes deployed by a different pipeline and coordination required | Singular pipeline handles all changes| 
|Infrastructure and Application skillset split across two teams | Developers more empowered with support from central cloud team |