#!/usr/bin/env python3

from aws_cdk import core
from awsboilerplate.pipeline.cdk_pipeline_stack import CDKPipelineStack
import awsboilerplate_config

app = core.App()

pipeline_stack = CDKPipelineStack(app, "awsboilerplate", env={
  'account': awsboilerplate_config.account,
  'region': awsboilerplate_config.region,
})


app.synth()
