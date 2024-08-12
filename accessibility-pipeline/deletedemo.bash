#!/bin/bash
# Bash file to delete the demo using CloudFormation 
# using the AWS CLI
#
read -p "Delete the CloudFormation Demo [y/n]? " yn

case "$yn" in 
	Y|y)
	echo "... thank you"
	;;
	*)
	echo "Enter 'Y' or 'y' to delete this demo"
	echo "... exiting"
	exit;
esac

# Parameters
REG=$(aws configure get region)
STACKNAME=DemoAccessibilityPipeline

# Validate Parameters
echo "... checking Region $REG"
if [[ "$REG" == "" ]]
then
	echo "... Region is $REG"
	echo "... exiting"
	exit;
fi

# Delete the stack
echo "... Deleting the CloudFormation Stack"
aws cloudformation delete-stack --stack-name $STACKNAME --region $REG --output json

# Wait for completion
echo "... waiting for CloudFormation Stack to be deleted"
aws cloudformation wait stack-delete-complete --stack-name $STACKNAME 

echo "... stack deleted."

# end
exit
