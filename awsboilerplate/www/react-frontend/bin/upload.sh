#!/bin/bash

#Manually upload (if cloud front cache is turned off this is a quick dev cycle vs running full codepipeline
aws s3 cp --recursive ./build s3://awsboilerplate.io --profile personal
