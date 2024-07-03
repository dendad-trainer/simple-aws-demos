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


## Setup Instructions ##
Copy the YML file into an S3 bucket. 

Log in to the AWS Console, and choose CloudFormation. Make sure you are in the same Region as before.

Create Resources from New, referencing the YML file.


## Demo Instructions ##
Look up the 'Outputs' Section of the CloudFormation Stack.
Use a browser to go to the HTTP:// of the Web Server in the Public Subnet. Show that this webserver returns its ImageId and AZ.
Go to VPC 


## Tidy Up ##
The following steps need to be performed to tidy up the infastructure at the end of the demo.

Log in to the AWS Console, choose CloudFormation and "Terminate" the Stack.
