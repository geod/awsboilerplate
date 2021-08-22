# Configuration for awsboilerplate. Used by cdk_pipeline_stack.py and app.py

# When you fork the repository point to your username/fork name
github_user = "geod"
github_repo = "awsboilerplate"
# NOTE - the github token is stored as a secret in secret manager

account = "390589559702"
region = "us-east-1"

stack_lambda_hello_world = True

#EXPERIMENTAL - flags enable creation of additional back end patterns
stack_lambda_background_worker_enabled = False
stack_lambda_redis_enabled = False
stack_lambda_s3processor_enabled = False

# Set once you register a domain in r53 and get the hosted zone
website_domain_name = "awsboilerplate.io"
hosted_zone_id = "Z0294872265LREBAVWK90"




