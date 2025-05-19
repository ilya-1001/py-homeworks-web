from fastapi import FastAPI
from schema import (CreateAdvertisementRequest, UpdateAdvertisementRequest, CreateAdvertisementResponse,
                    UpdateAdvertisementResponse, GetAdvertisementResponse, SearchAdvertisementResponse,
                    DeleteAdvertisementResponse, SuccessResponse)
from lifespan import lifespan
from dependancy import SessionDependency
from sqlalchemy import select
from constants import SUCCESS_RESPONSE
import models
import crud


app = FastAPI(
    title="Advertisement API",
    description="list of Advertisements",
    lifespan=lifespan
)


@app.post("/api/v1/advertisement", tags=["advertisement"], response_model=CreateAdvertisementResponse)
async def create_advertisement(advertisement: CreateAdvertisementRequest, session: SessionDependency):
    advertisement_dict = advertisement.model_dump(exclude_unset=True)
    advertisement_orm_obj = models.Advertisement(**advertisement_dict)
    await crud.add_item(session, advertisement_orm_obj)
    return advertisement_orm_obj.id_dict


@app.get("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"],
         response_model=GetAdvertisementResponse)
async def create_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_orm_obj = await  crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    return advertisement_orm_obj.dict


@app.get("/api/v1/advertisement", tags=["advertisement"], response_model=SearchAdvertisementResponse)
async def search_advertisement(session: SessionDependency,
                               title: str | None = None,
                               description: str | None = None,
                               price: float | None = None,
                               author: str | None = None):
    query = (
        select(models.Advertisement)
        .where((models.Advertisement.title == title) |
               (models.Advertisement.description == description) |
               (models.Advertisement.price == price) |
               (models.Advertisement.author == author))
        .limit(10000)
    )
    advertisements = await session.scalars(query)
    return {"results": [advertisement.dict for advertisement in advertisements]}


@app.patch("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"],
           response_model=UpdateAdvertisementResponse)
async def update_advertisement(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest,
                               session: SessionDependency):
    advertisement_dict = advertisement_data.model_dump(exclude_unset=True)
    advertisement_orm_obj = await crud.get_item_by_id(session,models.Advertisement, advertisement_id)

    for field, value in advertisement_dict.items():
        setattr(advertisement_orm_obj, field, value)
    await crud.add_item(session, advertisement_orm_obj)
    return SUCCESS_RESPONSE


@app.delete("/api/v1/advertisement/{advertisement_id}", tags=["advertisement"],
            response_model=DeleteAdvertisementResponse)
async def update_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    await crud.delete_item(session, advertisement_orm_obj)
    return SUCCESS_RESPONSE