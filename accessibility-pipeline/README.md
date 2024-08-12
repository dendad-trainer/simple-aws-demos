# Create a CodePipeline using Lambda to parse HTML files for accessibility testing

## Introduction ##
The CloudFormation Template creates the following AWS Resources:
- S3 bucket to store the input ZIP file
- target S3 bucket which CodePipeline will deploy to
- CodePipeline and associated S3 bucket
- Lambda function to parse HTML files for accessibility testing

This CodePipeline demo is used to illustrate the use of a Lambda function as one step in a pipeline. When using Lambda in a CodePipeline, it is necessary to post a message to the calling pipeline.

The source of the pipeline is an S3 bucket, which receives a ZIP file containg HTML source code.

The Lambda function is the main step in the pipeline. It unzips the file, extracts the HTML and parses each file for accessibility. 
By 'accessibility' in this case, we are looking for all the '<img' tags in the file. If there are no images, the file is marked as conforming to accessibility testing. If an image tag is found, the function looks for 'alt=' text. If this does not exist, the file is deemed to fail accessibility testing and the pipeline is halted.

If the pipeline step succeeds, the Lambda function posts a message directly to the CodePipeline, which proceeds to the next step.

The final stage of the pipeline is to deploy the ZIP file to the target S3 bucket.

## Pre-requisites ##
- A browser to connect to your AWS Account (recommended browsers are Chrome or Firefox)
- You can use the AWS CLI to launch the cloudformation template


## Setup Instructions ##
There are two ways of setting up the environment.

### Using the AWS Console ###
Log in to the AWS Console, and choose CloudFormation. Make sure you are in the AWS Region you want to create the demo in.

Create Resources from New, and select the CloudFormationAutoScaling.yaml file.

Check the 'Events' tab for progress. 
Check the 'Outputs' tab for the IP address of the Website and DNS Name of the Load Balancer.

### Using the AWS CLI (Linux or Mac) ###
Download the CloudFormationAutoScaling.yaml file and the builddemo.bash and deletedemo.bash files to your local directory.
At the command mode:
- chmod +x *.bash

Execute the builddemo.bash file:
- ./builddemo.bash

This is will build the CloudFormation stack, and wait until completion.

## Demo Instructions ##
(in progress)

## Tidy Up ##
The following steps need to be performed to tidy up the infastructure at the end of the demo.

Log in to the AWS Console, chose S3 and delete all contents from the S3 buckets, choose CloudFormation and "Terminate" the Stack.

Alternatively, from the Command line you can enter the following command:
- ./deletedemo.bash

In either case, you also need to do the following:
- In the AWS Console, go to S3 and locate the S3 bucket used by CloudFormation in that region (with a name such as 'cf-templates- '). Delete all files in this bucket to save storage costs.
- In the AWS Console, go to CloudWatch and choose "Logs". Delete all the CloudWatch Logs which contain the name 'DemoAccessibilityPipeline'.

## Summary of Files ##
| File | Purpose |
| ------ | ------- |
| CloudFormationAccessibilityCodePipeline.yaml | Cloud Formation Template to build the Stack of the complete Demo environment |
| html_checker.py | For Reference: Lambda Function to parse HTML files for accessibility (included in CloudFormation Template) |
| README.md | This file |
| builddemo.bash | Linux / Mac bash file to create the CloudFormation Stack for the Demo |
| deletedemo.bash | Linux / Mac bash file to delete the CloudFormation Stack after the Demo |



