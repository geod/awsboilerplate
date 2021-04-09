from aws_cdk import (core, aws_s3 as s3, aws_codebuild as codebuild, aws_codepipeline_actions as codepipeline_actions, aws_codepipeline as code_pipeline)
from aws_cdk.pipelines import CdkPipeline, CdkStage
from aws_cdk.pipelines import SimpleSynthAction
from .cdk_stage import UBStage
import startuptoolbag_config


# TODO / Manual Fiddles to IAM that I need to put in code
# - Had to give codebuild both cloudformation & staging bucket access
# https://stackoverflow.com/questions/57118082/what-iam-permissions-are-needed-to-use-cdk-deploy
# https://github.com/aws/aws-cdk/issues/6808
# bucket.grant_read_write(pipeline.role)
# Had to grant codebuild ability to search for VPCs/List when I started to add elasticache and vpc
# https://github.com/aws/aws-cdk/issues/1898

################################################################################
# Create the CDK pipeline.
# Its kind of a bad API - you have to create a 'special/explicit/CDK' type of pipeline rather than an arbitrary pipeline that has a synth stage
#
# However, by using this special CDKPipeline codepipeline will create mutate stages and additional behavior (dynamically mutate it)
# https://aws.amazon.com/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/
# https://github.com/aws/aws-cdk

# Real world tips and tricks: https://medium.com/swlh/aws-cdk-pipelines-real-world-tips-and-tricks-part-1-544601c3e90b
################################################################################

################################################################################
# The above handles the 'bootstrap' of the pipeline. It only mutates the pipeline.
# It does not create or execute entirety of CDK
# You can now add more STAGES which in turn can define STACKS / Actions
################################################################################

# Note Stage is set of stacks (variables can not cross stages. This is different than stacks)
# OMG - this is nasty - https://medium.com/swlh/aws-cdk-pipelines-real-world-tips-and-tricks-part-1-544601c3e90b

# TODO - v2 seems to be BitBucketSourceAction - https://github.com/aws/aws-cdk/issues/11582
# Makes a mutuable pipeline (updates itself) https://www.youtube.com/watch?v=1ps0Wh19MHQ


class CDKPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.source_output = code_pipeline.Artifact()
        source_action = codepipeline_actions.GitHubSourceAction(action_name="GitHub_Source",
                                                                owner=startuptoolbag_config.github_user,
                                                                repo=startuptoolbag_config.github_repo,
                                                                oauth_token=core.SecretValue.secrets_manager(
                                                                    'startuptoolbag-github-oath-token'),
                                                                output=self.source_output,
                                                                branch='master')

        # Note - this is an additional artifact per https://gist.github.com/JelsB/cff41685f12613d23a00951ce1531dbb
        application_code = code_pipeline.Artifact('application_code')
        cloud_assembly_artifact = code_pipeline.Artifact('cloudformation_output')

        synth_action = SimpleSynthAction(
            source_artifact=self.source_output,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_command='npm install -g aws-cdk && pip install -r requirements.txt',
            synth_command='cdk synth',
            additional_artifacts=[{'artifact': application_code, 'directory': './'}])

        self.cdk_pipeline = CdkPipeline(self, "tub-pipeline-project",
                                        cloud_assembly_artifact=cloud_assembly_artifact,
                                        source_action=source_action,
                                        synth_action=synth_action)

        # Can not be updated as it is in use by the sub stack
        bucket_name = startuptoolbag_config.website_domain_name if startuptoolbag_config.website_domain_name != "" else None
        www_site_bucket = s3.Bucket(
            self,
            f'WWW2_Bucket_{startuptoolbag_config.website_domain_name}',
            bucket_name=bucket_name,
            website_index_document='index.html',
            website_error_document='error.html',
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Creates infrastructure including cloudfront and the public facing bucket
        ub_stage = UBStage(self, "cdk-stage")
        cdk_stage = self.cdk_pipeline.add_application_stage(ub_stage)

        # Now need to build react and deploy
        # Challenges
        # 1. Cant get the bucket out of the stage
        # 2. Cant put the codebuild into the stage
        # 3. Cant create react build as a separate stage
        # 4. Cant export the bucket as a variable because the import attempts to run before the stage is synthesized


        build_output_artifact = code_pipeline.Artifact()
        codebuild_project = codebuild.PipelineProject(
            self, "tub-CDKCodebuild",
            project_name="tub-CodebuildProject",
            build_spec=codebuild.BuildSpec.from_source_filename(filename='buildspec.yml'),
            environment=codebuild.BuildEnvironment(privileged=True),
            description='React Build',
            timeout=core.Duration.minutes(60),
        )

        self.build_action = codepipeline_actions.CodeBuildAction(action_name="ReactBuild",
                                                                 project=codebuild_project,
                                                                 input=application_code,
                                                                 outputs=[build_output_artifact])

        self.s3_deploy = codepipeline_actions.S3DeployAction(action_name="ReactS3Push",
                                                             input=build_output_artifact,
                                                             bucket=www_site_bucket)

        self.cdk_pipeline.code_pipeline.add_stage(stage_name="ReactBuild", actions=[self.build_action])
        self.cdk_pipeline.code_pipeline.add_stage(stage_name="ReactDeploy", actions=[self.s3_deploy])

        self.output = core.CfnOutput(
            self, "WWWSITEBUCKETNAME", export_name="WWWSITEBUCKETNAME",
            value=www_site_bucket.bucket_name
        )
        props = {'namespace': 'cdk-example-pipeline'}
        self.output_props = props.copy()
        self.output_props['WWWSITEBUCKETNAME'] = www_site_bucket