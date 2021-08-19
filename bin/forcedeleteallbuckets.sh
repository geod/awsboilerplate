#!/bin/bash

# Sometimes a stack fails to delete.

aws s3api list-buckets \
   --query 'Buckets[?starts_with(Name, `awsboilerplate`) == `true`].[Name]' \
   --output text --profile personal | xargs -I {} aws s3 rb s3://{} --force --profile personal
