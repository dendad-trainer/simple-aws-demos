# Demo CodePipeline using Lambda to parse HTML files for accessibility testing

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
Once the pipeline has been created in cloudFormation, it will attempt to run. The SOURCE Phase will fail because there is no ZIP file to process. You can ignore this behaviour.

You then need to create a ZIP file with some web pages. There are examples attached (see table below). The web pages should be zipped into the ROOT directory of the ZIP file. 

The ZIP file, by default, should be called 'SampleApp_Linux.zip'. (This can be changed when you launch the CloudFormation template). 

Upload this ZIP file to the testing bucket (default name = testing-bucket-demo1). This will start the pipeline, which will execute the Lambda function during the INVOKE Phase. The Lambda function will unzip the file, and open each of the html files in turn. If an html file has an 'img' tag, then the file will be marked as 'Failed" unless there is also a 'alt=' tag. 

If any of the files fail the test, the CodePipeline will be stopped. 

If all of the files pass the test, the CodePipeline will proceeed to the DEPLOY Phase, which will deploy all the html files onto the target S3 bucket (default name = home-bucket-demo1). 

Experiment with different combinations of files.

### Other features to demonstrate ####
Look at the source code of the Lambda function (html_checker) and note the payload contents that are unpacked when the function is called, and the posting to the CodePipeline JOB on completion.

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
| webpage-img-alt.html | Example webpage with img tag and alt descriptor |
| webpage-img-both.html | Example webpage with img tag and alt descriptor and img tag without |
| webpage-img-noalt.html | Example webpage with img tag but without alt descriptor |
| webpage-noimg.html | Example webpage without any img tags | 


