#!/bin/bash
# Bash file to build the demo using CloudFormation 
# using the AWS CLI
#
read -p "Build the Demo using CloudFormation [y/n]? " yn

case "$yn" in 
	Y|y)
	echo "... thank you"
	;;
	*)
	echo "Enter 'Y' or 'y' to build this demo"
	echo "... exiting"
	exit;
esac

# Parameters
REG=$(aws configure get region)
FILENAME=CloudFormationAccessibilityCodePipeline.yaml
STACKNAME=DemoAccessibilityPipeline

# Validate Parameters
echo "... checking Region $REG"
if [[ "$REG" == "" ]]
then
	echo "... Region is $REG"
	echo "... exiting"
	exit;
fi
echo "... checking for File $FILENAME"
if [[ ! -f ./$FILENAME ]]
then
	echo "... $FILENAME not found"
	echo "... exiting"
	exit;
fi

# Create the stack
echo "... Creating the CloudFormation Stack"
aws cloudformation create-stack --stack-name $STACKNAME --region $REG --template-body file://$FILENAME --capabilities CAPABILITY_NAMED_IAM --output json

# Wait for completion
echo "... waiting for CloudFormation Stack to complete"
aws cloudformation wait stack-create-complete --stack-name $STACKNAME 

# Display the outputs
echo "... stack build complete. Outputs:"
aws cloudformation describe-stacks --stack-name $STACKNAME --region $REG --query "Stacks[].{Name:StackName,Status:StackStatus}" --output table

aws cloudformation describe-stacks --stack-name $STACKNAME --region $REG --query "Stacks[].Outputs[].{Key:OutputKey,Val:OutputValue}" --output table

# end
exit
