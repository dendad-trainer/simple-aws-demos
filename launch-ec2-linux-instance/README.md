# How to Launch a Linux-based Amazon EC2 Instance

## Introduction ##
The CloudFormation Template creates the following AWS Resources:
- An Amazon EC2 instance running Apache webserver
- A Security Group allowing access via HTTP and SSH only from all locations

In addition, you need to create an EC2 Keypair for security authentication. This has to be done manually before running the CloudFormation Template.

## Pre-requisites ##
- A browser to connect to your AWS Account (recommended browsers are Chrome or Firefox)
- A terminal application such as PuTTY (for Windows laptops) or Terminal (for Mac or Linux Laptops)


## Instructions ##
Log in to the AWS Console, and choose EC2. Make sure you know which Region you are in. Note down the Region Name for later reference.
Choose Keypair and create a new Keypair. Download the PEM file into a folder in your Laptop. Make a note of the Keypair name (e.g. 'example-linux-keypair')

Copy the YML file into an S3 bucket. 

Log in to the AWS Console, and choose CloudFormation. Make sure you are in the same Region as before.

Create Resources from New. 

Reference the S3 bucket where the YML file is stored. 

## Validation ##
This is where we validate the resources you have created.


## Tidy Up ##
The following steps need to be performed to tidy up the infastructure at the end of the demo.

1. Log in to the AWS Console, choose CloudFormation and "Terminate" the Stack.
2. From the AWS Console, choose S3 and delete the YML file from the S3 bucket. 
3. If required, delete the S3 bucket.
4. From the AWS Console, choose EC2 and delete the EC2 Keypair.
5. Delete the Private keypair PEM file from your own Laptop.
