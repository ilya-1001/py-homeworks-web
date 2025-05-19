from typing import Literal
from pydantic import  BaseModel
import datetime


class IdResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal["success"]


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: float
    author: str


class CreateAdvertisementResponse(IdResponse):
    id: int


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None


class UpdateAdvertisementResponse(SuccessResponse):
    pass


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    date_of_creation: datetime.datetime


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class DeleteAdvertisementResponse(SuccessResponse):
    pass