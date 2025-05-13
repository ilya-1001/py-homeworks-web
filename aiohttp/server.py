import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Session, Ad, close_orm, init_orm

app = web.Application()


async def orm_context(app: web.Application):
    print("STARTED")
    await init_orm()
    yield
    print("FINISHED")
    await close_orm()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(err_cls, message: str | dict | list):
    json_response = json.dumps({"error": message})
    return err_cls(text=json_response, content_type="application/json")


async def get_ad_by_id(ad_id: int, session: AsyncSession) -> Ad:
    ad = await session.get(Ad, ad_id)
    if ad is None:
        raise get_error(web.HTTPNotFound, "ad not found")
    return ad


async def add_ad(ad: Ad, session: AsyncSession):
    try:
        session.add(ad)
        await session.commit()
    except IntegrityError:
        raise get_error(web.HTTPConflict, "ad already exist")


class AdView(web.View):

    @property
    def ad_id(self) -> int:
        return int(self.request.match_info["ad_id"])

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get_ad(self) -> Ad:
        return await get_ad_by_id(self.ad_id, self.session)

    async def get(self):
        ad = await self.get_ad()
        return web.json_response(ad.dict)

    async def post(self):
        ad_data = await self.request.json()
        ad = Ad(
            title=ad_data["title"], description=ad_data["description"],
            owner=ad_data["owner"]
        )
        await add_ad(ad, self.session)
        return web.json_response(ad.id_dict)

    async def patch(self):
        data = await self.request.json()
        ad = await self.get_ad()

        if "title" in data:
            ad.title = data["title"]
        if "description" in data:
            ad.description = data["description"]
        if "owner" in data:
            ad.owner = data["owner"]

        await add_ad(ad, self.session)

        return web.json_response(ad.id_dict)

    async def delete(self):
        ad = await self.get_ad()
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({"status": "deleted"})


app.add_routes(
    [
        web.post("/ads", AdView),
        web.get("/ads/{ad_id:[0-9]+}", AdView),
        web.patch("/ads/{ad_id:[0-9]+}", AdView),
        web.delete("/ads/{ad_id:[0-9]+}", AdView),
    ]
)

web.run_app(app)