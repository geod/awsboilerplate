#!/usr/bin/env python3

from aws_cdk import core
from startuptoolbag.pipeline.cdk_pipeline_stack import CDKPipelineStack
import startuptoolbag_config

app = core.App()

pipeline_stack = CDKPipelineStack(app, "startuptoolbag-app", env={
  'account': startuptoolbag_config.account,
  'region': startuptoolbag_config.region,
})


app.synth()
