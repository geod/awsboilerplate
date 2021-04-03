# from aws_cdk import (
#     aws_s3 as s3,
# )
# from aws_cdk.core import RemovalPolicy
# import aws_cdk.aws_codebuild as codebuild
# import aws_cdk.aws_codepipeline_actions as codepipeline_actions
# import aws_cdk.aws_codepipeline as codepipeline
#
# from aws_cdk.aws_s3 import Bucket
# from aws_cdk import core
#
#
# class ReactStack(core.Stack):
#     """
#         Contains
#             - Certificate
#             - Cloudfront Distribution => Static Bucket
#             - DNS to route API.example.com => API GW
#             - Redirect from example.com to www.example.com
#
#         Stack Emits two constructs
#         A) Static Bucket which is used later in the deploy
#         B) API Gateway used by subsequent stacks
#     """
#
#     def __init__(self, scope: core.Construct, id: str, source_output: codepipeline.Artifact, site_bucket: Bucket,
#                  code_pipeline: codepipeline.Pipeline, **kwargs):
#         super().__init__(scope, id, **kwargs)
#
#         # Could refactor the bucket to be part of the stage
#
#         # https://github.com/aws-samples/aws-cdk-examples/blob/master/typescript/static-site/static-site.ts
#         # Need to move to a stack / into tub
#         # The codebuild project can be moved back out into the pipeline (bit awkward?)
#
#         self.react_site_bucket = s3.Bucket(self, 'ReactSiteBucket',
#                                            website_index_document="index.html",
#                                            website_error_document="error.html",
#                                            public_read_access=True,
#                                            removal_policy=RemovalPolicy.RETAIN)
#
#         self.build_output_artifact = codepipeline.Artifact()
#
#         build_output_artifact = codepipeline.Artifact()
#
#         codebuild_project = codebuild.PipelineProject(
#             self, "t-u-b-CDKCodebuild",
#             project_name="t-u-b-CodebuildProject",
#             build_spec=codebuild.BuildSpec.from_source_filename(filename='buildspec.yml'),
#             environment=codebuild.BuildEnvironment(privileged=True),
#             description='Pipeline for the-ultimate-boilerplate',
#             timeout=core.Duration.minutes(60),
#         )
#
#         build_action = codepipeline_actions.CodeBuildAction(action_name="ReactBuild",
#                                                             project=codebuild_project,
#                                                             input=source_output,
#                                                             outputs=[build_output_artifact])
#
#         s3_deploy = codepipeline_actions.S3DeployAction(action_name="ReactS3Push",
#                                                         input=build_output_artifact,
#                                                         bucket=site_bucket)
#
#         # Would be more elegant to be one stage but the input to deploy must be created in a prior stage
#         code_pipeline.add_stage(stage_name="ReactBuild", actions=[build_action])
#         code_pipeline.add_stage(stage_name="ReactDeploy", actions=[s3_deploy])
#
#
