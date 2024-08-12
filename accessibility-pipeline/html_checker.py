# HTML CHECKER
# Python Code to check HTML files for <> tags and basic accessibility checking.
# For demo purposes.
# This only checks for <IMG tags, and whether they have ALT= descriptors.
# Note that only one failure breaks the process and returns "False"
#

from __future__ import print_function

import boto3
import os
import fnmatch
import sys 
import zipfile

# Entry point for code when hosted in AWS Lambda
def lambda_handler(event, context):
	# unpack event parameters from CodePipeline
	jobId = event['CodePipeline.job']['id']
	s3location = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['bucketName']
	s3object = event['CodePipeline.job']['data']['inputArtifacts'][0]['location']['s3Location']['objectKey']
	print("S3 Bucket: " + str(s3location) + ", Object: " + str(s3object))
	
	# copy and unpack the source files and run assessment
	targetfolder = copy_zip_to_tmp(s3location,s3object)
	allcodeok = check_all_html_files(targetfolder)
	finalmsg = "Final Code Assessment: Accessible code: " + str(allcodeok)
	print(finalmsg)
	
	# Notify CodePipeline job
	code_pipeline = boto3.client('codepipeline')
	if (allcodeok == True):
		print('Putting job success')
		code_pipeline.put_job_success_result(jobId=jobId)
	else:
		print('Putting job failure')
		code_pipeline.put_job_failure_result(jobId=jobId, failureDetails={'message': finalmsg, 'type': 'JobFailed'})

	# end of handler
	print('End of handler')
	return finalmsg

# Copies the ZIP file to the /tmp directory and unpacks it
# Parameters:
#	name of bucket containing the ZIP file
#	name of the zip file itself
# Returns
#	location of the /tmp directory where the files are
def copy_zip_to_tmp(s3bucket, s3object):
	tmpfolder = '/tmp'
	writefilename = tmpfolder + "/sourcecode.zip"
	print (f"Copying s3://{s3bucket}/{s3object} to {writefilename}")
	# Copy zip file to temporary folder
	s3 = boto3.client('s3')
	try:
		with open(writefilename,'wb') as writef:
			s3.download_fileobj(s3bucket,s3object,writef)
	except Exception as e:
		print("ERROR: S3 operation failed")
		print(str(e))
	# Unpack the zip file
	try:
		with zipfile.ZipFile(writefilename,'r') as zip_ref:
			zip_ref.extractall(path=tmpfolder)
		print(f"Extracted {writefilename} to {tmpfolder}")
	except zipfile.BadZipFile:
		print(f"ERROR: {writefilename} is not a valid zip file")
	return tmpfolder

# Reads the directory to find all HTML files and processes them
# Parameters:
#	File directory to walk through
# Returns:
#	True if all files pass accessibility test
#	False if any file buffer returns a False accessibilty
def check_all_html_files(osdir):
	allfilesok = True
	filesfound = []
	# Build an array of HTML file names in this directory
	print ("Reading Directory: ",osdir)
	for htmlfound in os.listdir(osdir):
		if fnmatch.fnmatch(htmlfound,"*.html"):
			filesfound.append(htmlfound)
	# Iterate through the files and check each in turn
	if (len(filesfound) == 0):
		print("No files found to process")
	for ff in filesfound:
		filebuff = open_this_file(osdir+"/"+ff)
		res = check_html_for_img(filebuff)
		if (res == False):
			allfilesok = False
			break
	return allfilesok

# Opens the file and returns a file buffer
# Parameters:
#	nextfile = name of file to open
# Returns:
# 	filebuff = file buffer 
def open_this_file(nextfile):
	print ("Opening file: ",nextfile)
	f = open(nextfile, "r")
	filebuff = f.read()
	f.close()
	return filebuff

# Parses the buffer of HTML text, looking for IMG and ALT tags
# Parameters:
#	fbuffer = buffer of HTML code from a file read
# Returns: 
# 	True if there are no "<img" tags at all
# 	True if every "<img" tag has an "alt=" attribute
# 	False if there are "<img" tags without an "alt=" attribute
def check_html_for_img(fbuffer):
	imgvalid = True
	startpos = 0
	# find the first IMG tag
	tagpos1 = fbuffer.find("<img",startpos)
	while (tagpos1 != -1):
		# find the corresponding end tag
		endtagpos = fbuffer.find(">",tagpos1)
		print("Evaluating: ",fbuffer[tagpos1:endtagpos+1])
		# is there an ALT between them
		findalt = fbuffer.find(" alt=",tagpos1,endtagpos)
		if (findalt == -1):
			imgvalid = False
			print("Evaluation: - cannot find an alt string")
			break
		else:
			print ("Evaluation - found an alt string")
		# find the next IMG tag from the end of the last one
		tagpos1 = fbuffer.find("<img",endtagpos)
	print ("Buffer Assessment: Accessible code: ", imgvalid)
	return imgvalid

# Driver code for inline testing
if __name__ == '__main__':
	# argv[1] = name of the S3 bucket where the archive exists
	# argv[2] = name of the ZIP file in the bucket
	if ((len(sys.argv)) == 3):
		# unpack event parameters from CodePipeline
		s3location = sys.argv[1]
		s3object = sys.argv[2]
		print("S3 Bucket: " + str(s3location) + ", Object: " + str(s3object))
		
		# copy and unpack the source files and run assessment
		targetfolder = copy_zip_to_tmp(s3location,s3object)
		allcodeok = check_all_html_files(targetfolder)
		finalmsg = "Final Code Assessment: Accessible code: " + str(allcodeok)
		print(finalmsg)
	else:
		print ("ERROR: Invalid number of arguments")
