from beanie import Document, init_beanie, PydanticObjectId
from datetime import datetime

class Nippo(Document):
    _id :PydanticObjectId
    user_id: PydanticObjectId
    event_id : PydanticObjectId
    contents: str
    good: list
    bookmark: list
    purpose: str
    customer: str
    chat_log_id: PydanticObjectId
    timestamp: datetime

    class Settings:
        name = "nippo"
        

class Event(Document):
    _id :  PydanticObjectId
    user_id: PydanticObjectId
    customer: str
    chatlog_id: PydanticObjectId
    # nippo_id: PydanticObjectId
    start_time: datetime
    end_time: datetime
    address: str
    
    class Settings:
        name = "event"


