from typing import Optional, Union

from pydantic import BaseModel, validator
import datetime


class JobToDatabaseSchema(BaseModel):
    user: str
    console_command: Optional[str] = None
    start_at: Optional[Union[str, datetime.datetime]] = None
    executed_at: Optional[str] = None
    completed: Optional[bool] = False
    canceled: Optional[bool] = False


class JobToTerminal(BaseModel):
    console_command: str
    start_at: Optional[Union[str, datetime.datetime]] = None
    executed_at: Optional[Union[str, datetime.datetime]] = None

    @validator("start_at", "executed_at", pre=True)
    def return_string_from_datetime(cls, v):
        if v is None:
            return v
        return v.strftime("%Y-%m-%d %H:%M:%S")



class JobFromDatabaseSchema(BaseModel):
    id: int
    user: str
    console_command: str
    start_at: Union[str, datetime.datetime]
    executed_at: Optional[str] = None
    completed: Optional[bool] = False
    canceled: Optional[bool] = False
