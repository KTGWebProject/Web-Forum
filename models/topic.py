from typing import Annotated, Optional
from pydantic import BaseModel, StringConstraints
from models.reply import Reply
from datetime import datetime


class TopicResponse(BaseModel):
    content: str
    username: str
    created: datetime | None = None # = None only for local testing, to be removed later!!!
    upvotes: int
    downvotes: int
    is_best: bool

    @classmethod
    def replies_from_query_results(cls, content, username, created, upvotes, downvotes, is_best):
        return cls(content=content, 
                   username=username, 
                   created=created,
                   upvotes=upvotes,
                   downvotes=downvotes,
                   is_best=is_best)


class Topic(BaseModel):
    id: Optional[int] = None
    title: Annotated[str, StringConstraints(min_length=2, max_length=200)]
    created_on: datetime | None = None # = None only for local testing, to be removed later!!!
    text: Annotated[str, StringConstraints(min_length= 10, max_length=1000)]
    category_id: int
    author_id: Optional[int | str | None] = None
    replies: Optional[list[TopicResponse]] | Optional[int] = []
    is_locked: bool = False


    @classmethod
    def from_query_result(cls, id, title, created_on, text, category_id, author_id, replies, is_locked):
        return cls(id=id,
                   title=title,
                   created_on=created_on, 
                   text=text, 
                   category_id=category_id, 
                   author_id=author_id,
                   replies=replies,
                   is_locked=is_locked)
    
    @classmethod
    def cat_from_query_result(
        cls,
        id = None,
        title = None,
        created_on = None,
        text = None,
        category_id = None,
        author_name = None,
        replies = None,
        access_status = None,
    ):
        return cls(
            id=id,
            title=title,
            created_on=created_on,
            text=text,
            category_id=category_id,
            author_id=author_name,
            replies=replies,
            access_status=access_status,
        )