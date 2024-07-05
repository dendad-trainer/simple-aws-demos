import boto3
import cfnresponse
def handler(event, context):
# Init ...
rtype = event['RequestType']
print("The event is: ", str(rtype) )

responseData = {}
ec2api = boto3.client('ec2')
image_available_waiter = ec2api.get_waiter('image_available')

# Retrieve parameters
instanceId = event['ResourceProperties']['InstanceId']

# Main processing block
try:
if rtype in ('Delete', 'Update'):
  # deregister the AMI and delete the snapshot
  print ("Getting AMI ID")
  res = ec2api.describe_images( Filters=[{'Name': 'name', 'Values': ['DemoWebServerAMI']}])

  print ("De-registering AMI")
  ec2api.deregister_image( ImageId=res['Images'][0]['ImageId'] )

  print ("Getting snapshot ID")
  res = ec2api.describe_snapshots( Filters=[{'Name': 'tag:Name', 'Values': ['DemoWebServerSnapshot']}])

  print ("Deleting snapshot")
  ec2api.delete_snapshot( SnapshotId= res['Snapshots'][0]['SnapshotId'] )
  responseData['SnapshotId']=res['Snapshots'][0]['SnapshotId']

if rtype in ('Create', 'Update'):
  # create the AMI
  print ("Creating AMI and waiting")
  res = ec2api.create_image( 
    Description='Demo AMI created for autoscaling group',
    InstanceId=instanceId,
    Name='DemoWebServerAMI',
    NoReboot=True,
    TagSpecifications=[ {'ResourceType': 'image',
      'Tags': [ {'Key': 'Name', 'Value': 'DemoWebServerAMI'} ]},
        {'ResourceType': 'snapshot',
        'Tags': [ {'Key': 'Name', 'Value': 'DemoWebServerSnapshot'} ]}]
  )
  image_available_waiter.wait ( ImageIds=[res['ImageId']] )
  responseData['ImageId']=res['ImageId']

# Everything OK... send the signal back
print("Operation successful!")
cfnresponse.send(event,
                context,
                cfnresponse.SUCCESS,
                responseData)
except Exception as e:
  print("Operation failed...")
  print(str(e))
  responseData['Data'] = str(e)
  cfnresponse.send(event,
                  context,
                  cfnresponse.FAILED,
                  responseData)
#return True

