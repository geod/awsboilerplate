from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_codepipeline as code_pipeline,
                     aws_iam,
                     aws_s3)
from aws_cdk.aws_codebuild import Cache
from aws_cdk.pipelines import CdkPipeline, SimpleSynthAction
from awsboilerplate.infra.lambda_webapp_cdk_stage import LambdaWebArchitectureCDKStage
import awsboilerplate_config


class CDKPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.source_output = code_pipeline.Artifact()
        source_action = codepipeline_actions.GitHubSourceAction(action_name="GitHub_Source",
                                                                owner=awsboilerplate_config.github_user,
                                                                repo=awsboilerplate_config.github_repo,
                                                                oauth_token=core.SecretValue.secrets_manager(
                                                                    'awsboilerplate-github-oath-token'),
                                                                output=self.source_output,
                                                                branch='master')

        """
        The pipeline we want to create handles all of application, infrastructure, monitoring and pipeline
        Source -> Synth -> Self Mutate Pipeline -> Build Application Artifacts -> CDK Assets -> CDK Deploy
        
        CDK does not currently natively support mixing application and infrastructure builds in a single pipeline.
        To achieve a single combined pipeline we have to wire this together in a non-standard way and jump through a few hoops.
        
        Constraints that need to be followed:
        - All application build artifacts must be created after the pipeline mutates and before CDK constructs
        - We are not allowed to pass constructs from outside CDK stages into CDK stages.
        - We can 'sneak' build artifacts from the local filesystem into the CDK Stage
        
        Rather than following the standard examples and creating a CDK Pipeline from the outset we need to create a standard
        code pipeline and add the CDK features onto that pipeline
        """

        self.code_pipeline = code_pipeline.Pipeline(self, f"{construct_id}-codepipeline-project",
                                                    restart_execution_on_update=True,
                                                    stages=[code_pipeline.StageProps(stage_name="Source",
                                                                                     actions=[source_action])])

        """
        To add application builds we add a codebuild project to the pipeline. The one twist is that the project
        leaves build artifacts on the local filesystem of codepipeline. 

        We are going to pull these artifacts from this path and deploy to S3 within the CDK stage later in the pipeline
        (this is why the application artifact builds need to run before the CDK stages)
        """
        post_react_build_artifact = self.add_react_build(construct_id, self.code_pipeline, self.source_output)

        application_code = code_pipeline.Artifact('application_code')
        cloud_assembly_artifact = code_pipeline.Artifact('cloudformation_output')
        synth_action = SimpleSynthAction(
            # source_artifact=self.source_output,post_react_build_artifact
            source_artifact=post_react_build_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_command='npm install -g aws-cdk && pip install -r requirements.txt',
            synth_command='cd $CODEBUILD_SRC_DIR && cdk synth',
            additional_artifacts=[{'artifact': application_code, 'directory': './'}])


        """
        Adds CDK stages to the existing pipeline
        CDK pipelines stages added include 1) self-mutate on changes to this file 2) allows deployment of CDK constructs
        """
        self.cdk_pipeline = CdkPipeline(self, f"{construct_id}-cdk-pipeline",
                                        cloud_assembly_artifact=cloud_assembly_artifact,
                                        code_pipeline=self.code_pipeline,
                                        synth_action=synth_action,
                                        self_mutating=True)

        env = {
            'account': awsboilerplate_config.account,
            'region': awsboilerplate_config.region,
        }
        """
        Application stages in CDK are misleadingly named. They are meant to be self-contained environments (beta, prod)
        The stage deploys the full set of constructs (API GW, CloudFront, Lambdas, Dynamo, etc)
        """
        prod_app_stage = LambdaWebArchitectureCDKStage(self, f"{construct_id}-prod", env=env,
                                                       domain_name=awsboilerplate_config.website_domain_name,
                                                       hosted_zone_id=awsboilerplate_config.hosted_zone_id)
        prod_stage = self.cdk_pipeline.add_application_stage(prod_app_stage)

    def add_react_build(self, parent_construct_id, c_pipeline: code_pipeline.Pipeline, application_code: code_pipeline.Artifact):
        cache_bucket = aws_s3.Bucket(self, "ReactCodeBuildCache")
        build_output_artifact = code_pipeline.Artifact()
        # https://docs.aws.amazon.com/codebuild/latest/userguide/setting-up.html
        codebuild_project = codebuild.PipelineProject(
            self,
            f"{parent_construct_id}-react-codebuild",
            project_name=f"{parent_construct_id}-react-codebuild",
            build_spec=codebuild.BuildSpec.from_source_filename(filename='buildspec.yml'),
            environment=codebuild.BuildEnvironment(privileged=True),
            description='React Build',
            cache=Cache.bucket(cache_bucket),
            timeout=core.Duration.minutes(15)
        )

        build_action = codepipeline_actions.CodeBuildAction(action_name="ReactBuild",
                                                            project=codebuild_project,
                                                            input=application_code,
                                                            outputs=[build_output_artifact],
                                                            environment_variables={
                                                                "FOO": codebuild.BuildEnvironmentVariable(value="BAR")})

        c_pipeline.add_stage(stage_name="ReactBuild", actions=[build_action])
        return build_output_artifact
