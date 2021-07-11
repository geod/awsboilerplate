from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_s3 as s3,
    aws_route53 as route53,
    aws_certificatemanager as certificatemanager,
    aws_apigateway,
    core,
    aws_route53,
    aws_route53_patterns,
    aws_route53_targets,
    aws_s3_deployment as s3deploy
)
import startuptoolbag_config


class RawCloudFrontStack(core.Stack):
    """
        Contains
            - Cloudfront Distribution => Static Bucket
            - API GW

        Stack Emits two constructs
        A) Static Bucket which is used later in the deploy
        B) API Gateway used by subsequent stacks
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        bucket_name = startuptoolbag_config.website_domain_name if startuptoolbag_config.website_domain_name != "" else None
        self.www_site_bucket = s3.Bucket(
            self,
            f'WWW2_Bucket_{startuptoolbag_config.website_domain_name}',
            bucket_name=bucket_name,
            website_index_document='index.html',
            website_error_document='error.html',
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        s3deploy.BucketDeployment(self, "DeployWebsite",
                                  sources=[s3deploy.Source.asset("./www/react-boilerplate/build")],
                                  destination_bucket=self.www_site_bucket,
                                  #destination_key_prefix="./"
                                  )

        www_source_configuration = cloudfront.SourceConfiguration(
            s3_origin_source=cloudfront.S3OriginConfig(
                s3_bucket_source=self.www_site_bucket
            ),
            behaviors=[cloudfront.Behavior(is_default_behavior=True)]
        )

        www_distribution = cloudfront.CloudFrontWebDistribution(
            self,
            'SiteDistribution',
            origin_configs=[www_source_configuration]
        )

        self.rest_api = aws_apigateway.RestApi(self, 'RestApiGateway', deploy=False)
        api_domain_name = f'api.{startuptoolbag_config.website_domain_name}'


class CloudFrontStack(core.Stack):
    """
        Contains
            - Certificate
            - Cloudfront Distribution => Static Bucket
            - DNS to route API.example.com => API GW
            - Redirect from example.com to www.example.com

        Stack Emits two constructs
        A) Static Bucket which is used later in the deploy
        B) API Gateway used by subsequent stacks
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # note assumption zone is named after domain
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(self, "HostedZone",
                                                                     hosted_zone_id=startuptoolbag_config.hosted_zone_id,
                                                                     zone_name=startuptoolbag_config.website_domain_name)

        # SSL/TLS Certificate
        # https://github.com/aws/aws-cdk/pull/8552
        # Experimental vs 'Certificate' (which requires validation in the console)
        tls_cert = certificatemanager.DnsValidatedCertificate(
            self,
            "SiteCertificate",
            hosted_zone=hosted_zone,
            domain_name=f'*.{startuptoolbag_config.website_domain_name}',
            subject_alternative_names=[startuptoolbag_config.website_domain_name],
            region='us-east-1',
        )

        bucket_name = startuptoolbag_config.website_domain_name if startuptoolbag_config.website_domain_name != "" else None
        self.www_site_bucket = s3.Bucket(
            self,
            f'WWW2_Bucket_{startuptoolbag_config.website_domain_name}',
            bucket_name=bucket_name,
            website_index_document='index.html',
            website_error_document='error.html',
            public_read_access=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        s3deploy.BucketDeployment(self, "DeployWebsite",
                                  sources=[s3deploy.Source.asset("./www/react-boilerplate/build")],
                                  destination_bucket=self.www_site_bucket,
                                  #destination_key_prefix="./"
                                  )

        # # Import the bucket that was created outside the stack
        # self.www_site_bucket = s3.Bucket.from_bucket_name(self, 'SiteBucket', core.Fn.import_value("WWWSITEBUCKETNAME"))

        # CloudFront distribution that provides HTTPS - for www
        www_alias_configuration = cloudfront.AliasConfiguration(
            acm_cert_ref=tls_cert.certificate_arn,
            names=[f'www.{startuptoolbag_config.website_domain_name}'],
            ssl_method=cloudfront.SSLMethod.SNI,
            security_policy=cloudfront.SecurityPolicyProtocol.TLS_V1_1_2016
        )

        www_source_configuration = cloudfront.SourceConfiguration(
            s3_origin_source=cloudfront.S3OriginConfig(
                s3_bucket_source=self.www_site_bucket
            ),
            behaviors=[cloudfront.Behavior(is_default_behavior=True)]
        )

        www_distribution = cloudfront.CloudFrontWebDistribution(
            self,
            'SiteDistribution',
            alias_configuration=www_alias_configuration,
            origin_configs=[www_source_configuration]
        )

        route53.ARecord(
            self,
            'CloudFrontARecord',
            zone=hosted_zone,
            record_name=f'www.{startuptoolbag_config.website_domain_name}', #site domain
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.CloudFrontTarget(www_distribution))
        )

        # NAKED site bucket which redirects to naked to www
        redirect = aws_route53_patterns.HttpsRedirect(self, 'NakedRedirect',
                                                      record_names=[startuptoolbag_config.website_domain_name],
                                                      target_domain=f'www.{startuptoolbag_config.website_domain_name}',
                                                      zone=hosted_zone,
                                                      certificate=tls_cert)

        # Create the API Gateway
        self.rest_api = aws_apigateway.RestApi(self, 'RestApiGateway', deploy=False)
        api_domain_name = f'api.{startuptoolbag_config.website_domain_name}'
        domain = self.rest_api.add_domain_name('APIDomain', certificate=tls_cert, domain_name=api_domain_name)

        route53.ARecord(
            self,
            'APIGWAliasRecord',
            zone=hosted_zone,
            record_name=api_domain_name, #site domain
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGatewayDomain(domain))
        )


class APIGatewayDeployStack(core.Stack):
    """
        When breaking up API GW between stacks the pattern is to add a stack at the end of the stage to finalize deployment
        https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigateway-readme.html#breaking-up-methods-and-resources-across-stacks
    """
    def __init__(self, scope: core.Construct, id: str, api_gateway: aws_apigateway.RestApi, **kwargs):
        super().__init__(scope, id, **kwargs)
        deployment = aws_apigateway.Deployment(self, 'APIGWDeployment', api=api_gateway)
        map(lambda m: deployment.node.add_dependency(m), api_gateway.methods)
        stage = aws_apigateway.Stage(self, 'Stage', deployment=deployment, stage_name='prod')