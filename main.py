from fastapi import FastAPI
from pydantic import BaseModel
from starlette.exceptions import HTTPException
from tortoise.contrib.fastapi import register_tortoise

from models import Items, Item_Pydantic, ItemIn_Pydantic


app = FastAPI()


class Status(BaseModel):
    message: str


@app.post("/items/", response_model=Item_Pydantic)
async def create_item(item: ItemIn_Pydantic):
    item_obj = await Items.create(**item.model_dump())
    return await Item_Pydantic.from_tortoise_orm(item_obj)


@app.get("/items/", response_model=list[Item_Pydantic])
async def get_items():
    return await Item_Pydantic.from_queryset(Items.all())


@app.get("/items/{item_id}", response_model=Item_Pydantic)
async def get_item(item_id: int):
    return await Item_Pydantic.from_queryset_single(Items.get(id=item_id))


@app.put("/items/{item_id}", response_model=Item_Pydantic)
async def update_item(item_id: int, item: ItemIn_Pydantic):
    await Items.filter(id=item_id).update(**item.model_dump())
    return await Item_Pydantic.from_queryset_single(Items.get(id=item_id))


@app.delete("/items/{item_id}", response_model=Status)
async def delete_item(item_id: int):
    deleted_count = await Items.filter(id=item_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return Status(message=f"Deleted Item {item_id}")


register_tortoise(
    app,
    db_url="sqlite://./database.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
