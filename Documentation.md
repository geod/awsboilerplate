## Background / Design Goals and Anti-Goals

### The Problem

The core problem is the time and complexity to integrate and assemble a fully featured development
and deployment architecture.

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