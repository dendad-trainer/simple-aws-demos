#!/bin/bash -ex
# Use latest Amazon Linux 2023
dnf update -y
dnf install -y httpd php-fpm php php-devel
/usr/bin/systemctl enable httpd
/usr/bin/systemctl start httpd
cd /var/www/html
cat <<EOF > index.php
<?php
?>
<!DOCTYPE html>
<html>
  <head>
    <title>Amazon AWS Demo Website</title>
  </head>
  <body>
  <h2>Amazon AWS Demo Website</h2>
  <table border=1>
  <tr><th>Meta-Data</th><th>Value</th></tr>
<?php
  # Get the instance ID
  echo "<tr><td>InstanceId</td><td><i>";
  echo shell_exec('ec2-metadata --instance-id');
  "</i></td><tr>";
  # Instance Type
  echo "<tr><td>Instance Type</td><td><i>";
  echo shell_exec('ec2-metadata --instance-type');
  "</i></td><tr>";
  # AMI ID
  echo "<tr><td>AMI</td><td><i>";
  echo shell_exec('ec2-metadata --ami-id');
  "</i></td><tr>";
  # User Data
  echo "<tr><td>User Data</td><td><i>";
  echo shell_exec('ec2-metadata --user-data');
  "</i></td><tr>";
  # Availability Zone
  echo "<tr><td>Availability Zone</td><td><i>";
  echo shell_exec('ec2-metadata --availability-zone');
  "</i></td><tr>";
?>
  </table>
  </body>
</html>
EOF
# Sleep to ensure that the file system is synced before the snapshot is taken
sleep 120
# Signal to say its OK to create an AMI from this Instance.
/opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --region ${AWS::Region} --resource AMICreate
