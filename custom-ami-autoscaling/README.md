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
Look up the 'Outputs' Section of the CloudFormation Stack (or look at the Outputs of the bash file) to get the IP address of the WebServer, and the DNS Name of the Application Load Balancer.

#### Investigate Webserver ####
Use a browser to go to the HTTP:// IP Address of the Web Server in the Public Subnet.
Show that this webserver returns its ImageId and AZ.
This Webserver has been built using "User Data", as you can see from the output.
The Webserver resides in a Public Subnet and has it's own IP public IP address. 

If you go to the AWS Console, you can see the WebServer, and demonstrate that it is in a Public Subnet.
You should be able to use "EC2 Connect" to connect to this WebServer, and show the webserver command line. You can enter the "ec2-metadata --all" command to show the configuration of this webserver. Enter the command "ec2-metadata --user-data" to show that the Apache webserver was installed, and the index.php file created. 
You can also reference the AWS AMI that was used to build this webserver.

#### Investigate AutoScaling Group ####
Use a browser to go to the HTTP:// DNSName of the Load Balancer.
Show that this returns a webserver with its ImageId and AZ.
Refresh the Browser, and you will see a different webserver, with a different ImageId and AZ.
As a quiz question, get people to work out how many webservers there actually are.

Each Webserver has been built using a the same Custom AMI, and does not have any User Data. 
This is because the Custom AMI has been created from a Snapshot of the first WebServer.

If you go to the AWS Console, you can see the EC2 instances which comprise the AutoScaling Group. Note that each of these EC2 instances has identical names. Demonstrate that each of them is in a Private Subnet, and does not have an IP address itself. Instead, traffic is terminated at the Load Balancer, and forwarded to each of the target EC2 instances by the Application Loadbalancer.
Note that you are not able to use "EC2 Connect" to connect to any of these AutoScaling WebServers, because they do not have their own IP addresses.
Show the custom AMI which was used to build the AutoScaling group. 
Show the EC2 Snapshot that was taken of the original webserver, and used to build the AMI.

Also in the AWS Console, you can demonstrate the configuration of the Launch Template that is used by the AutoScaling Group. Show that this references the new AMI, and the Private Subnets to launch the new EC2 instances in.
The AutoScaling Group specifies the Minimum, Maximum and currently Desired number of EC2 instances.
The Application Webserver hosts the DNS name, and forwards traffic to the TargetGroup of EC2 instances.

## Tidy Up ##
The following steps need to be performed to tidy up the infastructure at the end of the demo.

Log in to the AWS Console, choose CloudFormation and "Terminate" the Stack.

Alternatively, from the Command line you can enter the following command:
- ./deletedemo.bash

In either case, you also need to do the following:
- In the AWS Console, go to S3 and locate the S3 bucket used by CloudFormation in that region (with a name such as 'cf-templates- '). Delete all files in this bucket to save storage costs.
- In the AWS Console, go to CloudWatch and choose "Logs". Delete all the CloudWatch Logs which contain the name 'DemoAMIBuilderFunction'.

## Summary of Files ##
| File | Purpose |
| ------ | ------- |
| CloudFormationAutoScaling.yaml | Cloud Formation Template to build the Stack of the complete Demo environment |
| DemoAMIBuilderFunction.py | For Reference: Lambda Function to build the AMI from the WebServer (included in CloudFormation Template) |
| README.md | This file |
| builddemo.bash | Linux / Mac bash file to create the CloudFormation Stack for the Demo |
| deletedemo.bash | Linux / Mac bash file to delete the CloudFormation Stack after the Demo |
| userdata.bash | For Reference: The UserData for the WebServer (included in CloudFormation Template) |



