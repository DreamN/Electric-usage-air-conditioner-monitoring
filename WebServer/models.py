import datetime
import psycopg2
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from settings import getDatabaseString


Base = declarative_base()
engine = create_engine(getDatabaseString())
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Device(Base):
    __tablename__ = 'device'
    id = Column(String(20), primary_key=True)
    status = Column(Boolean, default=False)
    aircon = Column(Boolean, default=False)
    totalTime = Column(BigInteger, default = 0)
    last_update = Column(DateTime, default = datetime.datetime.utcnow)

    def __init__(self, id):
        print('Registed device id : ' + id)
        self.id = id

    def update(self, status, aircon):
        self.status = status
        self.aircon = aircon
        if(self.status == False):
            timediff = datetime.datetime.utcnow - self.last_update
            self.totalTime += timediff
        self.last_update = datetime.datetime.utcnow


Base.metadata.create_all(engine)