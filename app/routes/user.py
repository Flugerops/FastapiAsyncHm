from sqlalchemy import select
from fastapi import HTTPException
from .. import app
from ..db import Session, User
from ..schemas import UserData


@app.get("/users")
async def get_users():
    async with Session.begin() as session:
        users = await session.scalars(select(User))
        users = [UserData.model_validate(user) for user in users]
        return users


@app.post("/users", status_code=201)
async def create_user(data: UserData):
    try:
        async with Session.begin() as session:
            user = User(**data.model_dump())
            session.add(user)
    except:
        raise HTTPException(400, detail="User already exist")


@app.delete("/users/{name}")
async def delete_user(name: str):
    async with Session.begin() as session:
        user = await session.scalar(select(User).where(User.name == name))
        if not user:
            raise HTTPException(404, detail="User not found")
        await session.delete(user)