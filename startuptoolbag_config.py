# Configuration for startuptoolbag. Used by cdk_pipeline_stack.py and app.py

github_user = "geod"
github_repo = "startup-toolbag"
# NOTE - the github token is stored as a secret in secret manager

account = "390589559702"
region = "us-east-1"

stack_lambda_redis_enabled = False
stack_lambda_webarchitecture_enabled = True
stack_lambda_s3processor_enabled = True

# IF NOT set then the project will create a deployment without a domain name
# IF SET then the project will automatically create cloud front distributions, DNS for etc for the domain
website_domain_name = "awsboilerplate.io"  # "awsboilerplate.io"
hosted_zone_id = "Z0294872265LREBAVWK90"

beta_environment = False




