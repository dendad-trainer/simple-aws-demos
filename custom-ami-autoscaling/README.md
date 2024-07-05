# Create a custom AMI and AutoScaling Group with Load Balancer

## Introduction ##
The CloudFormation Template creates the following AWS Resources:
- A VPC with two Public Subnets, two Private Subnets, NAT Gateway and routing tables.
- An Amazon EC2 instance running Apache webserver in a Public Subnet, accessible by HTTP. This webserver is built using specific UserData
- An EBS Snapshot and Custom AMI from the webserver above.
- A Launch Template based on the Custom AMI
- An Application Load Balancer, and AutoScaling group using the Launch Template


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
Look up the 'Outputs' Section of the CloudFormation Stack.
Use a browser to go to the HTTP:// of the Web Server in the Public Subnet. Show that this webserver returns its ImageId and AZ.
Go to VPC 


## Tidy Up ##
The following steps need to be performed to tidy up the infastructure at the end of the demo.

Log in to the AWS Console, choose CloudFormation and "Terminate" the Stack.
