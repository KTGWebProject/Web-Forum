from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Reply(BaseModel):
    id: Optional[int] | None = None
    content: str
    topic_id: int
    user_id: Optional[int] | None = None
    created_on: datetime
    is_best: bool = False 
    upvotes: int = 0
    downvotes: int = 0

    @classmethod
    def from_query_result(cls, id, content, topic_id, user_id, created_on, is_best):
        return cls(id=id,
                   content=content,
                   topic_id=topic_id,
                   user_id=user_id,
                   created_on=created_on,
                   is_best=is_best)
    

class Vote(int, Enum):
    up = 1 #'upvote'
    down = -1 #'downvote'
    remove = 0 #'remove vote'