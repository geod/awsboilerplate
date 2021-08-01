import os
from aws_cdk import (
    core,
    aws_lambda,
    aws_iam,
    aws_dynamodb,
    aws_ec2 as ec2,
    aws_apigateway,
    aws_s3,
    aws_sqs,
    aws_elasticache as elasticache,
    aws_s3_notifications
)
import aws_cdk.aws_lambda_event_sources as eventsources
import startuptoolbag_config
from .cloudfront_stack import FlexibleCloudFrontStack, APIGatewayDeployStack


class LambdaWebArchitectureCDKStage(core.Stage):

    def __init__(self, scope: core.Construct, id: str, domain_name=None, hosted_zone_id=None, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.cloud_front_stack = FlexibleCloudFrontStack(self, 'CloudFrontStack', domain_name, hosted_zone_id, **kwargs)

        if startuptoolbag_config.stack_lambda_redis_enabled:
            self.lambda_redis_stack = LambdaRedisStack(self, 'LambdaRedisStack',
                                                       api_gateway=self.cloud_front_stack.rest_api,
                                                    **kwargs)

        if startuptoolbag_config.stack_lambda_webarchitecture_enabled:
            self.lambda_sns_stack = LambdaWebArchitectureStack(self, 'LambdaWebArchitectureStack',
                                                               api_gateway=self.cloud_front_stack.rest_api,
                                                               **kwargs)

        if startuptoolbag_config.stack_lambda_s3processor_enabled:
            self.lambda_data_stack = LambdaS3DataPipelineStack(self, 'LambdaS3DataPipelineStack',
                                                               api_gateway=self.cloud_front_stack.rest_api,
                                                               **kwargs)

        self.deploy_stack = APIGatewayDeployStack(self, 'APIDeployStack',
                                                  api_gateway=self.cloud_front_stack.rest_api)


class LambdaS3DataPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, api_gateway: aws_apigateway.RestApi, **kwargs):
        super().__init__(scope, id, **kwargs)

        raw_bucket = aws_s3.Bucket(self, 'DataPipelineRawBucket',
                                   public_read_access=False,
                                   removal_policy=core.RemovalPolicy.DESTROY)

        processed_bucket = aws_s3.Bucket(self, 'DataPipelineProcessedBucket',
                                         public_read_access=False,
                                         removal_policy=core.RemovalPolicy.DESTROY)

        # Simple 1 step data pipeline - raw_bucket => lambda_processor => processed_bucket
        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory=os.path.join(os.getcwd(), "startuptoolbag/app/lambda_s3_processor"))
        lambda_processor = aws_lambda.Function(self,
                                               id="lambdaS3DataProcessor",
                                               description="Processes Data Landed In S3",
                                               code=ecr_image,
                                               handler=aws_lambda.Handler.FROM_IMAGE,
                                               runtime=aws_lambda.Runtime.FROM_IMAGE,
                                               environment={'RAW_BUCKET': raw_bucket.bucket_name,
                                                            'PROCESSED_BUCKET': processed_bucket.bucket_name},
                                               memory_size=128,
                                               reserved_concurrent_executions=1,
                                               timeout=core.Duration.seconds(900))

        notification = aws_s3_notifications.LambdaDestination(lambda_processor)
        raw_bucket.add_event_notification(aws_s3.EventType.OBJECT_CREATED, notification)

        raw_bucket.grant_read(lambda_processor)
        processed_bucket.grant_read_write(lambda_processor)

        # API Lambda which is backed by data in S3
        # This is essentially an Object Lambda - https://aws.amazon.com/blogs/aws/introducing-amazon-s3-object-lambda-use-your-code-to-process-data-as-it-is-being-retrieved-from-s3/
        # TODO investigate when CDK support ObjectLambda or CDK Solutions Patterns
        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory=os.path.join(os.getcwd(), "startuptoolbag/app/lambda_s3_server"))
        lambda_handler = aws_lambda.Function(self,
                                             id="lambdaS3Server",
                                             description="Handle API requests backed by S3",
                                             code=ecr_image,
                                             handler=aws_lambda.Handler.FROM_IMAGE,
                                             runtime=aws_lambda.Runtime.FROM_IMAGE,
                                             environment={'BUCKET': processed_bucket.bucket_name},
                                             memory_size=128,
                                             reserved_concurrent_executions=1,
                                             timeout=core.Duration.seconds(10))
        processed_bucket.grant_read(lambda_handler)

        foo_r = api_gateway.root.add_resource("data")
        foo_r.add_method('GET', aws_apigateway.LambdaIntegration(lambda_handler))


class LambdaWebArchitectureStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, api_gateway: aws_apigateway.RestApi, **kwargs):
        super().__init__(scope, id, **kwargs)

        # create dynamo table
        job_table = aws_dynamodb.Table(
            self, "demo_table",
            partition_key=aws_dynamodb.Attribute(
                name="job_id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # Create the Queue
        sqs_queue = aws_sqs.Queue(self, "SQSQueue")
        lambda_sqs_role = aws_iam.Role(self, id='lambda-sqs-role',
                                       assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
                                       managed_policies=[aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                           'service-role/AWSLambdaBasicExecutionRole'),
                                           aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                               'service-role/AWSLambdaSQSQueueExecutionRole')])

        # Lambda to accept background job requests
        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory=os.path.join(os.getcwd(), "startuptoolbag/app/lambda_sqs_handler"))
        background_task_acceptor_lambda = aws_lambda.Function(self,
                                                      id="lambdaTaskRequestHandlerFunction",
                                                      description="Handles/Valdates background requests and puts on SQS",
                                                      code=ecr_image,
                                                      handler=aws_lambda.Handler.FROM_IMAGE,
                                                      runtime=aws_lambda.Runtime.FROM_IMAGE,
                                                      environment={'SQS_NAME': sqs_queue.queue_name},
                                                      role=lambda_sqs_role,
                                                      allow_public_subnet=True,
                                                      memory_size=128,
                                                      reserved_concurrent_executions=10,
                                                      timeout=core.Duration.seconds(10))
        sqs_queue.grant_send_messages(background_task_acceptor_lambda)

        # Create the Background Worker (to calculate)
        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory=os.path.join(os.getcwd(), "startuptoolbag/app/lambda_sqs_bworker"))
        background_job_worker_lambda = aws_lambda.Function(self,
                                                  id="lambdaBackgroundWorker",
                                                  description="Pulls from SQS and is a background worker",
                                                  code=ecr_image,
                                                  handler=aws_lambda.Handler.FROM_IMAGE,
                                                  runtime=aws_lambda.Runtime.FROM_IMAGE,
                                                  environment={'SQS_NAME': sqs_queue.queue_name,
                                                               'TABLE_NAME': job_table.table_name},
                                                  role=lambda_sqs_role,
                                                  allow_public_subnet=True,
                                                  memory_size=128,
                                                  reserved_concurrent_executions=10,
                                                  timeout=core.Duration.seconds(10))
        background_job_worker_lambda.add_event_source(eventsources.SqsEventSource(sqs_queue))
        background_job_worker_lambda.add_environment("TABLE_NAME", job_table.table_name)
        job_table.grant_write_data(background_job_worker_lambda)

        # Create the Lambda Serving Job Results
        ecr_image = aws_lambda.EcrImageCode.from_asset_image(
            directory=os.path.join(os.getcwd(), "startuptoolbag/app/lambda_dynamodb_server"))
        background_job_result_lambda = aws_lambda.Function(self,
                                              id="lambdaResultProvider",
                                              description="Serves requests from Dynamo",
                                              code=ecr_image,
                                              handler=aws_lambda.Handler.FROM_IMAGE,
                                              runtime=aws_lambda.Runtime.FROM_IMAGE,
                                              environment={'TABLE_NAME': job_table.table_name},
                                              role=lambda_sqs_role,
                                              allow_public_subnet=True,
                                              memory_size=128,
                                              reserved_concurrent_executions=10,
                                              timeout=core.Duration.seconds(10))
        job_table.grant_read_data(background_job_result_lambda)

        # Route the API gateway to the correct handlers
        foo_r = api_gateway.root.add_resource("job")
        foo_r.add_method('POST', aws_apigateway.LambdaIntegration(background_task_acceptor_lambda))
        foo_r.add_method('GET', aws_apigateway.LambdaIntegration(background_job_result_lambda))



class LambdaRedisStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, api_gateway: aws_apigateway.RestApi, **kwargs):
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, id="default", is_default=True)

        self.redis = self.create_redis(vpc)

        ecr_image = aws_lambda.EcrImageCode.from_asset_image(directory=os.path.join(os.getcwd(),
                                                                                    "startuptoolbag/app/lambda_redis"))

        lambda_vpc_role = aws_iam.Role(self, id='lambda-vpc-role2',
                                       assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
                                       managed_policies=[aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                           'service-role/AWSLambdaBasicExecutionRole'),
                                           aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                                               'service-role/AWSLambdaVPCAccessExecutionRole')])

        lambda_function = aws_lambda.Function(self,
                                              id="lambdaRedisContainerFunction",
                                              description="LambdaRedisFunction",
                                              code=ecr_image,
                                              handler=aws_lambda.Handler.FROM_IMAGE,
                                              runtime=aws_lambda.Runtime.FROM_IMAGE,
                                              environment={"CACHE_ADDRESS": self.redis.attr_redis_endpoint_address,
                                                           "CACHE_PORT": self.redis.attr_redis_endpoint_port},
                                              role=lambda_vpc_role,
                                              vpc=vpc,
                                              allow_public_subnet=True,
                                              memory_size=128,
                                              reserved_concurrent_executions=10,
                                              timeout=core.Duration.seconds(10))

        foo_r = api_gateway.root.add_resource("cache")
        foo_r.add_method('GET', aws_apigateway.LambdaIntegration(lambda_function))

    def create_redis(self, vpc: ec2.IVpc):
        selection = vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)

        redis_security_group = ec2.SecurityGroup(self, id='redis-security-group', vpc=vpc)
        redis_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(6379), "Incoming to Redis")

        redis_subnet_group = elasticache.CfnSubnetGroup(
            self,
            "RedisClusterPrivateSubnetGroup",
            cache_subnet_group_name="redis-subnet-group",
            description="Tubby Redis Subnet",
            subnet_ids=selection.subnet_ids
        )

        redis_parameter_group = elasticache.CfnParameterGroup(
            self,
            "RedisParameterGroup",
            description="Redis Params",
            cache_parameter_group_family="redis6.x",
            properties={},
        )

        redis = elasticache.CfnCacheCluster(
            self,
            "RedisCacheCluster",
            engine="redis",
            cache_node_type="cache.t2.micro",
            num_cache_nodes=1,
            cluster_name="startuptoolbag-redis",
            vpc_security_group_ids=[redis_security_group.security_group_id],
            cache_subnet_group_name=redis_subnet_group.cache_subnet_group_name,
            cache_parameter_group_name=redis_parameter_group.ref,
        )
        return redis
