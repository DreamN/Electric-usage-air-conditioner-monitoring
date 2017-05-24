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


def dt_to_minutes(dt):
    days, hours, minutes = dt.days, dt.seconds // 3600, dt.seconds // 60 % 60
    return (days*24*60)+(hours*60)+minutes


class Device(Base):
    __tablename__ = 'device'
    id = Column(String(20), primary_key=True)
    status = Column(Boolean, default=False)
    aircon = Column(Boolean, default=False)
    totalTime = Column(BigInteger, default = 0)
    last_update = Column(DateTime, default = datetime.datetime.now())

    def __init__(self, id):
        print('Registed device id : ' + id)
        self.id = id

    def update(self, status, aircon):
        if(self.status and not status and self.aircon):   #if status on -> off && aircon on $AddTotal
            print("if status on -> off && aircon on $AddTotal")
            timediff = dt_to_minutes(datetime.datetime.now() - self.last_update)
            self.totalTime += timediff
            self.last_update = datetime.datetime.now()
        elif(self.status and self.aircon and not aircon): #if status on && aircon on -> off $AddTotal
            print("if status on && aircon on -> off $AddTotal")
            timediff = dt_to_minutes(datetime.datetime.now() - self.last_update)
            self.totalTime += timediff
            self.last_update = datetime.datetime.now()
        elif(not self.status and status and aircon):      #if status off -> on aircon on then update 
            print("if status on and aircon already on then update ")
            self.last_update = datetime.datetime.now()
        elif(self.status and not self.aircon and aircon):
            print("if status already on and aircon on then update ")
            self.last_update = datetime.datetime.now()           
        self.aircon = aircon
        self.status = status
        session.add(self)
        session.commit()

    def current_Total(self):
        current_Total = self.totalTime
        if self.aircon and self.status:
            timediff = dt_to_minutes(datetime.datetime.now() - self.last_update)
            current_Total += timediff
        return current_Total

    @property
    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'aircon': self.aircon,
            'totalTime': self.current_Total(),
            'last_update': self.last_update
        }


Base.metadata.create_all(engine)