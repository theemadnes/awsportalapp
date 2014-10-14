import boto.ec2

regionStrList = []

for i in boto.ec2.regions():
    regionStrList.append(str(i).split(':')[1])

regionIPlist = []

for i in regionStrList:
	conn = boto.ec2.connect_to_region(i)
	# get first IP
	eip = conn.allocate_address()
	regionIPlist.append(str(eip).split(':')[1])
	# rinse, repeat for second IP
	eip2 = conn.allocate_address()
	regionIPlist.append(str(eip2).split(':')[1])


instancetracker.cgd6ut3eybll.us-west-2.rds.amazonaws.com:3306
zip -r awsportalapp.zip .

# default
db = create_engine('mysql+pymysql://alex:testpassword@instancetracker.cgd6ut3eybll.us-west-2.rds.amazonaws.com/instanceTracker')


CREATE TABLE instances (
  sequence_id INTEGER NOT NULL AUTO_INCREMENT,
  instance_id CHAR(15) NOT NULL,
  instance_type CHAR(15) NOT NULL,
  availability_zone CHAR(20) NOT NULL,
  PRIMARY KEY (sequence_id)
);

# enable hidden files 
defaults write com.apple.finder AppleShowAllFiles TRUE


import boto.ec2
conn = boto.ec2.connect_to_region("us-west-2")

# dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType(snapshot_id='snap-d15cde24')
# dev_sda1.size = 10 # size in Gigabytes
dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType(snapshot_id='snap-d15cde24')
dev_sda1.volume_type='gp2'
bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
bdm['/dev/sda1'] = dev_sda1


dev_xvda = boto.ec2.blockdevicemapping.EBSBlockDeviceType(size=10)
dev_xvda.volume_type='gp2'
bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
bdm['/dev/xvda'] = dev_xvda

54.68.233.119

#return to use a reservation for the new instance
new_ec2_instance = conn.run_instances(image_id='ami-d13845e1', key_name='mattsona-051214', instance_type='t2.micro', security_groups=['SSH-DefaultVPC'], block_device_map = bdm)

# BlockDeviceMapping.n.Ebs.VolumeSize=10

new_ec2_instance = conn.run_instances(image_id='ami-d13845e1', key_name='mattsona-051214', instance_type='t2.micro', security_groups=['SSH-DefaultVPC'], BlockDeviceMapping.n.Ebs.VolumeSize=10 )

new_ec2_instance = conn.run_instances(image_id='ami-d13845e1', key_name='mattsona-051214', instance_type='t2.micro', security_groups=['SSH-DefaultVPC'])

## SQL commands
sqlite3 /tmp/instance_tracker.db < schema.sql


vpc-e6b70f83
i-1744d6f9 #1
i-ce691225
us-east-1


route #2
rtb-d03c84b5

"sudo -s echo 1 > /proc/sys/net/ipv4/ip_forward echo 0 > /proc/sys/net/ipv4/conf/eth0/send_redirects /sbin/iptables -t nat -A POSTROUTING -o eth0 -s 0.0.0.0/0 -j MASQUERADE /sbin/iptables-save > /etc/sysconfig/iptables mkdir -p /etc/sysctl.d/ echo net.ipv4.ip_forward = 1 >> /etc/sysctl.d/nat.conf echo net.ipv4.conf.eth0.send_redirects = 0 >>/etc/sysctl.d/nat.conf"
 (AWS 27)

AWS. Architecting on AWS Advanced Concepts 1.3 (EN): Lab Guide. AWS/Gilmore. VitalBook file.


