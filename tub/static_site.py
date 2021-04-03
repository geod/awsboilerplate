from aws_cdk.core import RemovalPolicy
import aws_cdk.aws_s3_deployment as s3_deployment
from aws_cdk.aws_s3 import Bucket
from aws_cdk import core


def add_static_site(stack: core.Stack):
    stack.static_site_bucket = Bucket(stack, 'StaticSiteBucket',
                                     website_index_document="index.html",
                                     website_error_document="error.html",
                                     public_read_access=True,
                                     removal_policy=RemovalPolicy.RETAIN)

    stack.static_bucket_deploy = s3_deployment.BucketDeployment(stack, "StaticSiteDeploy",
                                                              sources=[s3_deployment.Source.asset(
                                                                  "./www/static-site-content")],
                                                              destination_bucket=stack.static_site_bucket)