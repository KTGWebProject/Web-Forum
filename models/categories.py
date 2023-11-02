from pydantic import BaseModel, StringConstraints, Field
from datetime import datetime
from typing import Optional, Annotated


class Category(BaseModel):
    id: Optional[Annotated[int, Field(ge=1)]] | None = None
    name: Annotated[str, StringConstraints(min_length=1, max_length=45)]
    created_on: Optional[datetime] | None = None
    privacy_status: Optional[Annotated[str, StringConstraints(pattern="^(private|non_private)$")]] | None = "non_private"
    access_status: Optional[Annotated[str, StringConstraints(pattern="^(locked|unlocked)$")]] | None = "unlocked"

    @classmethod
    def from_query_result(cls, id, name, created_on, privacy_status, access_status):
        return cls(
            id=id,
            name=name,
            created_on=created_on,
            privacy_status=privacy_status,
            access_status=access_status,
        )

class PrivateCategory(BaseModel):
    id: int
    user: int
    write_access: bool


class CategoryResponseModel(BaseModel):  
    category_name: str
    created_on: datetime
    privacy_status: str
    category_id: int


class PrivilegedUsers(BaseModel):
    username: str
    access_level: str

    @classmethod
    def from_query_result(cls, username, access_level):
        return cls(username = username, access_level = access_level)