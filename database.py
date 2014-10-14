from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('mysql+pymysql://alex:testpassword@instancetracker.cgd6ut3eybll.us-west-2.rds.amazonaws.com/instanceTracker', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# Base.query = db_session.query_property()

# define Instances class
class Instance(Base):
	__tablename__ = 'instances'

	sequence_id = Column(Integer, primary_key=True)
	instance_id = Column(String)
	instance_type = Column(String)
	availability_zone = Column(String)

	def __init__(self, instance_id=None, instance_type=None, availability_zone=None):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.availability_zone = availability_zone

	def __repr__(self):
		return "<instance_id %r>" % (self.instance_id)


