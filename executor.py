import datetime
import time

from logic import Executor
from models.base import JobModel
from schemas.job_schema import JobFromDatabaseSchema

executor = Executor()

while True:
    time.sleep(1)
    with executor.SQLALCHEMY_SESSION() as session:
        jobs = session.query(JobModel).filter(JobModel.completed == False,
                                              JobModel.canceled == False
                                              ).order_by(JobModel.start_at.desc()
                                                         ).all()

        serialized_jobs = [JobFromDatabaseSchema(**job.__dict__) for job in jobs]

        for job in serialized_jobs:
            if datetime.datetime.now() >= job.start_at:
                executor.execute_job(job)

