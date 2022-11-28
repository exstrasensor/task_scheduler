import os
from datetime import datetime
from typing import Union, Optional, Any

from pydantic import BaseModel, validator, root_validator
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import JobModel
from schemas.job_schema import JobToDatabaseSchema, JobFromDatabaseSchema, JobToTerminal


class Executor(BaseModel):
    DATABASE_CREDENTIALS: Optional[Union[str]] = 'sqlite:///db'
    SQLALCHEMY_SESSION: Optional[Any] = None
    SQLALCHEMY_ENGINE: Optional[Any] = None

    @root_validator
    def compile_connections(cls, values):
        engine = create_engine(values["DATABASE_CREDENTIALS"])
        values["SQLALCHEMY_ENGINE"] = engine
        values["SQLALCHEMY_SESSION"] = sessionmaker(bind=engine)

        return values

    def execute_job(self, job_instance: JobFromDatabaseSchema):
        os.system(job_instance.console_command)
        with self.SQLALCHEMY_SESSION() as session:
            database_object = session.query(JobModel).where(JobModel.id == job_instance.id).first()
            setattr(database_object, "executed_at", datetime.datetime.now())
            setattr(database_object, "completed", True)
            session.flush()
            session.commit()


class JobScheduler(BaseModel):
    user: str
    console_command: Optional[Union[str, None]] = None
    start_at: Optional[Union[str, datetime.datetime, None]] = None

    DATABASE_CREDENTIALS: Optional[Union[str]] = 'sqlite:///db'
    SQLALCHEMY_SESSION: Optional[Any] = None
    SQLALCHEMY_ENGINE: Optional[Any] = None

    @root_validator
    def compile_connections(cls, values):
        engine = create_engine(values["DATABASE_CREDENTIALS"])
        values["SQLALCHEMY_ENGINE"] = engine
        values["SQLALCHEMY_SESSION"] = sessionmaker(bind=engine)

        return values

    @validator("start_at", pre=True)
    def convert_date_to_datetime(cls, v):
        if v is None:
            return v

        try:
            v = datetime.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            return v
        except Exception as e:
            raise e

    def create_job(self):
        validated_job = JobToDatabaseSchema(**self.dict())
        job_object = JobModel(**validated_job.dict())

        with self.SQLALCHEMY_SESSION() as session:
            session.add(job_object)
            session.commit()
            print(f"{validated_job.dict()} saved")

    def check_completed_jobs(self,
                             limit: int):

        with self.SQLALCHEMY_SESSION() as session:
            database_objects = session.query(JobModel).filter(JobModel.user == self.user,
                                                              JobModel.completed == True).limit(limit).all()
            for object in database_objects:
                yield JobToTerminal(**object.__dict__).dict()

    def check_scheduled_jobs(self,
                             limit: int):

        with self.SQLALCHEMY_SESSION() as session:
            database_objects = session.query(JobModel).filter(JobModel.user == self.user,
                                                              JobModel.completed == False).limit(limit).all()
            for object in database_objects:
                yield JobToTerminal(**object.__dict__).dict()



if __name__ == "__main__":
    vals = {
        "user": "a",
        "console_command": "sa",
        "start_at": "2022-01-01 12:01:01"
    }

    instance = JobScheduler(**vals)
    # print(instance.create_job())
    print(list(instance.check_completed_jobs(10)))