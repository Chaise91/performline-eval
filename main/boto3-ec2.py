import boto3

userData = '''#!/bin/bash
sudo yum update -y
sudo curl --output /usr/bin/eval-server.bin https://raw.githubusercontent.com/PerformLine/DevOpsEval/master/bin/eval-server.linux-x86_64
sudo chmod +x /usr/bin/eval-server.bin
sudo curl --output /etc/systemd/system/eval-server.service https://raw.githubusercontent.com/Chaise91/performline-eval/main/main/eval-server.service
sudo systemctl enable eval-server.service
sudo systemctl start eval-server.service
sudo iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8086'''

session = boto3.session.Session(profile_name='performline')
resource=session.resource('ec2', region_name="us-east-1")

#Create and configure security group

securityGroup=resource.create_security_group(GroupName="CCooper Eval",
                                    Description="Created by CCooper for eval")
                        
securityGroup.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=22,ToPort=22)
securityGroup.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=80,ToPort=80)
securityGroupdID=securityGroup.id
print(securityGroupdID)

#Import Provided keypair

keyPair=resource.import_key_pair (
    KeyName="ccooper-eval-kp",
    PublicKeyMaterial="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDOzStXtpDN2wRrIWCoWUNNFA+c4fd9v3Mne8EpU66L/W24NSlbsk8rlHWvdPduJBFqymHPnId99KRhYOERq2uD8AevDZc9J4WhAXgc9uxKabkBR01lnxOWRbRmwXvKDU4lNMJoiGE+jOG8wG3wpWLPZ9bhf6y3Ig7FUST4nt/R/Zrq3IVWy7qHYnwms7kGfs8sdDoGuRfqASYYgpZ8JRtGig0hRjc3GfMhT0yX6KM9wQWiORtr12ZVbzdhIeW/SKfUZ1vZaULaoo5n1b8BdNC/rNGRrf3zhZiZAoJ3avfePOTcuyUldcb21bxnXFGxIcXtxAoyEBSYQwGmWn4+WyN9"
)

#Create and configure EC2 instance

ec2 = boto3.resource('ec2')

instance=resource.create_instances(ImageId='ami-033b95fb8079dc481',InstanceType='t2.micro',UserData=userData,
                          KeyName='ccooper-eval-kp',MaxCount=1,MinCount=1,
                          NetworkInterfaces=[{'DeviceIndex':0,
                                              'AssociatePublicIpAddress': True,
                                              'Groups':[securityGroup.group_id]}])

instance[0].wait_until_running()
print(instance[0])
print("EC2 instance successfully created with along with new security group: 'CCooper Eval'")