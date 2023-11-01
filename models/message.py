from pydantic import BaseModel, constr, conint
from datetime import datetime
from typing import Optional



class Message(BaseModel):
    id: Optional[int] = None
    content: constr(min_length=1)
    created_on: Optional[datetime] = None
    subject: constr(min_length=1, max_length=45) = "No subject"
    id_parent_message: Optional[int] = None

class MessageResponseModelConversation(Message):
    author: str
    recipient: str

    @classmethod
    def get_response(cls, id, author, recipient, subject, content, created_on, id_parent_message):
        return cls(
            id = id,
            content = content,
            created_on = created_on,
            subject = subject,
            id_parent_message = id_parent_message,
            author = author,
            recipient = recipient            
        )
    
class MessageResponseModelChat(Message):
    author: str

    @classmethod
    def get_response_chat(cls, id, author, subject, content, created_on, id_parent_message):
        return cls(
            id = id,
            content = content,
            created_on = created_on,
            subject = subject,
            id_parent_message = id_parent_message,
            author = author            
        )