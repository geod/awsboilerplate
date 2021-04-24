import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
import aws_cdk.aws_codepipeline as codepipeline

from aws_cdk.aws_s3 import Bucket
from aws_cdk import core

def add_react_build(stack: core.Stack, code_pipeline, source_output, bucket_arn: str):
    # Could refactor the bucket to be part of the stage

    # https://github.com/aws-samples/aws-cdk-examples/blob/master/typescript/static-site/static-site.ts
    # Need to move to a stack / into startuptoolbag
    # The codebuild project can be moved back out into the pipeline (bit awkward?)

    react_site_bucket = Bucket.from_bucket_arn(stack, id='SiteBucket', bucket_arn=bucket_arn)
    stack.build_output_artifact = codepipeline.Artifact()
    build_output_artifact = codepipeline.Artifact()
    codebuild_project = codebuild.PipelineProject(
        stack, "t-u-b-CDKCodebuild",
        project_name="t-u-b-CodebuildProject",
        build_spec=codebuild.BuildSpec.from_source_filename(filename='buildspec.yml'),
        environment=codebuild.BuildEnvironment(privileged=True),
        description='Pipeline for the-ultimate-boilerplate',
        timeout=core.Duration.minutes(60),
    )

    build_action = codepipeline_actions.CodeBuildAction(action_name="ReactBuild",
                                                        project=codebuild_project,
                                                        input=source_output,
                                                        outputs=[build_output_artifact])

    s3_deploy = codepipeline_actions.S3DeployAction(action_name="ReactS3Push",
                                                    input=build_output_artifact,
                                                    bucket=react_site_bucket)

    # Would be more elegant to be one stage but the input to deploy must be created in a prior stage
    code_pipeline.add_stage(stage_name="ReactBuild", actions=[build_action])
    code_pipeline.add_stage(stage_name="ReactDeploy", actions=[s3_deploy])
