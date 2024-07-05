# simple-aws-demos
A collection of demos that illustrate some of the basic AWS services.

## Introduction ##
This repo contains a series of folders, each with an README.md for creating a stand-alone demo AWS environment that illustrates one basic aspect of AWS, such as launching an EC2 instance, or creating a VPC.

Typically, the work to create the environment is all handled by a CloudFormation template. 
However, some manual tasks may have to be performed in some cases.

Don't forget to delete the resources created by the manual tasks, and terminate the CloudFormation Stack after you have completed the Demo.

## Inventory of folders ##

| Folder | Purpose |
| ------ | ------- |
| create-multi-az-vpc | Creates a VPC across 3 AZ with Public, Private and Restricted Subnets |
| custom-ami-autoscaling | Builds a Custom AMI and AutoScaling Group with Loadbalancer |
| launch-ec2-linux-instance | Launches an Amazon EC2 instance running Linux with supporting Security Group and Keypair |
| launch-ec2-windows-instance | Launches an Amazon EC2 instance running Windows with supporting Security Group and Keypair |
| serverless-website | Builds a Serverless Web site with S3 and CloudFront (work in progress) |
