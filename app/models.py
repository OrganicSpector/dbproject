import sqlalchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base
import session as _session
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()
create_flag = False


class Satellite(Base):
    __tablename__ = 'satellite'
    satelliteId = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), index=True)
    country = Column(String(50))
    expireDate = Column(DateTime)
    orbitRadius = Column(Float)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class TVChannel(Base):
    __tablename__ = 'tvchannel'
    tvChannelId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(50))
    broadcastingLanguage = Column(String(50))
    country = Column(String(50))
    telecompany = Column(String(50))
    type = Column(String(50))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Broadcasting(Base):
    __tablename__ = 'broadcasting'
    broadcasting_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tvChannelId = Column(Integer, ForeignKey('tvchannel.tvChannelId'))
    satelliteId = Column(Integer, ForeignKey('satellite.satelliteId'))
    frequency = Column(Float)
    zoneStart = Column(Integer)
    zoneEnd = Column(Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


if create_flag:
    Base.metadata.create_all(_session.engine)
    print("Tables created successfully.")
