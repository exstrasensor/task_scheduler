from sqlalchemy import Column, Integer, Sequence, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JobModel(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    console_command = Column(String)
    start_at = Column(DateTime)
    executed_at = Column(DateTime)
    completed = Column(Boolean, default=False)
    canceled = Column(Boolean, default=False)

