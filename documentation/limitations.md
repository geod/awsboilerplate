## Limitations

### CDK
CDK is great / clearly the future. It is very close to being a super powerful developer experience. Given it is still relatively new
(and CDKPipeline is very new) there are a few issues I encountered:

1. Even for a simple archetype like `awsboilerplate` the pipeline time is between 10-20 minutes. Even if infrastructure changes are not being made
CDK is very slow to synthesize and confirm that no changes have been made. When infrastructure changes are made then 
it can significantly increase pipeline time. This made it painfully slow to build the initial stages of the project (particularly when I was making a lot of mistakes).
CDKPipeline seems to have fewer cache and performance speed ups in comparison to regular Codepipeline. I hope that AWS can make this faster over time
because if they could get the pipeline time down to <10 minutes it would be a fabulous development experience.

2. Current CDK is not really designed to accommodate the 'everything is code' pattern implemented in awsboilerplate.
CDK assumes that application artifacts have been built prior to CDKPipelines running. CDK is then able to 'deploy' those artifacts when
lambdas or buckets are created using [Bucket Deployment](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-deployment-readme.html). The goal of awsboilerplate was to have a **single** pipeline for everything. As a result,
awsboilerplate stretches (hacks) CDKPipeline API. 

`cdk_pipeline_stack.py` does some gymnastics. where it mixes codepipeline and cdkpipelines. The react build runs first taking the source artifact. 
The react build runs and creates an output artifact which is the combination of all source in git **and** the contents of www/build. The hack
is that this output artifact is wired into CDKPipeline as an **input** artifact (CDKPipeline generally takes the source as input. 
Here we switch the source for an artifact which includes pre-built artifacts).
There is probably a whole blog article covering the 6-7 significantly different designs that were explored each with pitfalls.

3. The goal was to make *all* changes self-mutating. Because of the limitations above the react build runs **before** CDK Synth.
This means that changes to the react build are not self-mutating and need to be manually deployed via `cdk deploy`. There is
a different design which will also make the react build self-mutating that is being evaluated.

4. CDK under the covers still gets translated into cloudformation. It can still be a bit 'delicate' and sometimes major
refactoring of infrastructure can fail to execute and I generally deleted and recreated the entire stack.

### AWS Native Developer Tooling
AWS native devops tools - codebuild and codepipeline could be faster and more developer friendly.
1. They give cryptic error messages. Example : if you create a codepipeline and the secret it relies on is not created it fails silent. No useful message. It just fails.
2. Its slow - simple builds are all 5-10 minutes. 
3. They are difficult to debug given limited access (I often created debug statement in the buildspec. Combined with the slow speed each dev cycle is 5-15 minutes