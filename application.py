# our imports
# from sqlalchemy import *
# from sqlalchemy import Column, Integer, String
import pymysql
import boto.ec2
import time
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# configuration params ***TO BE REPLACED VIA USERDATA***
DB_SERVER = 'instancetracker.cgd6ut3eybll.us-west-2.rds.amazonaws.com'
DB_PORT = 3306
DB_NAME = 'instanceTracker'
DEBUG = True
SECRET_KEY = 'development key'
DB_USERNAME = 'alex'
DB_PASSWORD = 'testpassword'
APP_USERNAME = 'admin'
APP_PASSWORD = 'password'
INSTANCE_TAG = 'AWS Portal App'

# connect to AWS
conn = boto.ec2.connect_to_region("us-west-2")

# define ec2 parameters for instances
dev_xvda = boto.ec2.blockdevicemapping.EBSBlockDeviceType(size=10,delete_on_termination=True)
dev_xvda.volume_type='gp2'
bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
bdm['/dev/xvda'] = dev_xvda

# set up distribution of availability zones
zones = conn.get_all_zones()
azStrList = []
for az in zones:
	azStrList.append(str(az).split(':')[1])

# create application
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	return pymysql.connect(host=app.config['DB_SERVER'], port=app.config['DB_PORT'], user=app.config['DB_USERNAME'], passwd=app.config['DB_PASSWORD'], db=app.config['DB_NAME'])

#def init_db():
#	with closing(connect_db()) as db:
#		with app.open_resource('schema.sql', mode='r') as f:
#			db.cursor().executescript(f.read())
#		db.commit

@app.before_request
def before_request():
	g.db = connect_db()
	# g.db.cur = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()	

@app.route('/')
def show_instances():
	cur = getattr(g, 'db', None).cursor()
	cur.execute('select instance_id, instance_type, availability_zone from instances order by sequence_id desc')
	instance_tracker = [dict(instance_id=row[0], instance_type=row[1], availability_zone=row[2]) for row in cur.fetchall()]
	return render_template('show_instances.html', instance_tracker=instance_tracker)


@app.route('/add_instance', methods=['POST'])
def add_instance():
	if not session.get('logged_in'):
		abort(401)

	#return to use a reservation for the new instance, selecting a "random" AZ to deploy to
	reservation_object = conn.run_instances(image_id='ami-d13845e1', key_name='mattsona-051214', instance_type='t2.micro', security_groups=['SSH-DefaultVPC'], block_device_map = bdm, placement = azStrList[(random.randint(0, len(azStrList) - 1))])

	# wait to submit DB entries so we have the data, and update to get DNS info
	time.sleep(2)
	reservation_object.instances[0].update()

	instance_id = reservation_object.instances[0].id
	instance_type = reservation_object.instances[0].instance_type
	availability_zone = reservation_object.instances[0].placement
	public_dns = reservation_object.instances[0].public_dns_name

	# tag the instance
	reservation_object.instances[0].add_tag("Name", INSTANCE_TAG)

	print instance_id
	print instance_type
	print availability_zone
	print "See below for dns"
	print public_dns

	# update the DB
	cur = getattr(g, 'db', None).cursor()
	cur.execute('insert into instances (instance_id, instance_type, availability_zone) values (\'%s\', \'%s\', \'%s\')' % (instance_id, instance_type, availability_zone))
	g.db.commit()

	flash('New instance ' + instance_id + ' was created')
	return redirect(url_for('show_instances'))

@app.route('/terminate_instance', methods=['POST'])
def terminate_instance():
	# parse instance name 
	instance_to_terminate = request.form['instance_id'].split()[1]

	# terminate the instance on ec2
	conn.terminate_instances(instance_ids=[instance_to_terminate])
	print 'Instance ' + instance_to_terminate + ' terminated.'

	# update the DB
	cur = getattr(g, 'db', None).cursor()
	cur.execute('delete from instances where instance_id=\'%s\'' % instance_to_terminate)
	g.db.commit()

	# render screen
	flash('Instance ' + instance_to_terminate + ' was terminated')
	return redirect(url_for('show_instances'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['APP_USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['APP_PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_instances'))
	return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('logged_in')
	flash('You were logged out')
	return redirect(url_for('show_instances'))

if __name__ == '__main__':
	app.run()

