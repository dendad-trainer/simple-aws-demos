# How to Launch a Linux-based Amazon EC2 Instance

## Introduction ##
The CloudFormation Template creates the following AWS Resources:
- An Amazon EC2 instance running Apache webserver
- A Security Group allowing access via HTTP and SSH only from all locations
- A Keypair for security authentication.


## Instructions ##
Copy the YML file into an S3 bucket. 

Log in to the AWS Console, and choose CloudFormation. Make sure you know which Region you are in.

Create Resources from New. 

Reference the S3 bucket where the YML file is stored. 
