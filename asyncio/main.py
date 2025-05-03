import asyncio
import datetime
from typing import Sequence

import aiohttp
from more_itertools import chunked

from models import Session, SwapiPeople, close_orm, init_orm, create_db_table, drop_db_table

MAX_REQUESTS = 5


async def create_filds(urls, session, fild="name"):
    filds = []
    for url in urls:
        async with session.get(url) as response:
            data = await response.json()
            filds.append(data[fild])
    return ', '.join(filds)


async def get_people(person_id, session):

    response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    if response.status == 404:
        return
    json_data = await response.json()
    pesron = {
        "id": person_id,
        "name": json_data["name"],
        "birth_year": json_data["birth_year"],
        "eye_color": json_data["eye_color"],
        "films": await create_filds(json_data["films"], session, fild="title"),
        "gender": json_data["gender"],
        "hair_color": json_data["hair_color"],
        "height": json_data["height"],
        "homeworld": await create_filds([json_data["homeworld"]], session),
        "mass": json_data["mass"],
        "skin_color": json_data["skin_color"],
        "species": await create_filds(json_data["species"], session),
        "starships": await create_filds(json_data["starships"], session),
        "vehicles": await create_filds(json_data["vehicles"], session),
    }
    return pesron


async def insert_people(people: Sequence[dict]):
    async with Session() as session:
        swapi_people_list = [SwapiPeople(**item) for item in people if item is not None]
        session.add_all(swapi_people_list)
        await session.commit()


async def main():
    await drop_db_table()
    await create_db_table()
    await init_orm()
    ids_chunks = chunked(range(1, 101), MAX_REQUESTS)

    async with aiohttp.ClientSession() as session:
        for id_chunk in ids_chunks:
            coros = [get_people(people_id, session) for people_id in id_chunk]
            people_json_list = await asyncio.gather(*coros)
            insert_people_coro = insert_people(people_json_list)
            insert_people_task = asyncio.create_task(insert_people_coro)
        all_tasks = asyncio.all_tasks()
        current_task = asyncio.current_task()
        all_tasks.remove(current_task)
        await asyncio.gather(*all_tasks)

    await close_orm()


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
