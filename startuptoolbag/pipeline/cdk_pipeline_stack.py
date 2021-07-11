from aws_cdk import (core, aws_s3 as s3, aws_codebuild as codebuild, aws_codepipeline_actions as codepipeline_actions, aws_codepipeline as code_pipeline)
from aws_cdk.pipelines import CdkPipeline
from aws_cdk.pipelines import SimpleSynthAction
from startuptoolbag.infra.cdk_stage import CDKStage
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
            build_command='cd www/react-boilerplate; npm install; npm run build; cd ../..',
            synth_command='cdk synth',
            additional_artifacts=[{'artifact': application_code, 'directory': './'}])

        self.cdk_pipeline = CdkPipeline(self, "startuptoolbag-pipeline-project",
                                        cloud_assembly_artifact=cloud_assembly_artifact,
                                        source_action=source_action,
                                        synth_action=synth_action)

        stk_stage = CDKStage(self, "cdk-stage")
        cdk_stage = self.cdk_pipeline.add_application_stage(stk_stage)