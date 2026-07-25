from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Success(BaseModel, Generic[T]):
    type: Literal["success"] = "success"
    data: T


class Failure(BaseModel):
    type: Literal["failure"] = "failure"
    error: str
    code: str
