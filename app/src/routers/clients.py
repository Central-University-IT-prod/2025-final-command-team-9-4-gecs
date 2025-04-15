from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_
from src import jwt, database, models, schemas, passwords
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import datetime
from datetime import timezone, timedelta


router = APIRouter(tags=["Clients"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/clients/login")

@router.post("/clients/new", status_code=201)
async def register_client(session: AsyncSession = Depends(database.db_get)):
    async with session.begin():
        db_item = models.Client()
        session.add(db_item)
        await session.flush()

    await session.refresh(db_item)
    token = jwt.create_jwt({"id": str(db_item.id)})

    return {
        "token": token
    }

@router.get("/clients/profile")
async def info_client(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    async with session.begin():
        user_data = jwt.decode_jwt(token)
        client = await database.query(session, models.Client, [models.Client.id == user_data["id"]], user=True)
        if (client.name, client.email, client.location, client.gender, client.age) is None:
            raise HTTPException(204)

    return {
        "name": client.name,
        "email": client.email,
        "location": client.location,
        "gender": client.gender,
        "age": client.age,
    }

@router.patch("/clients/profile")
async def edit_clients(info: schemas.ClientsEdit, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        client = await database.query(session, models.Client, [models.Client.id == user_data["id"]], False, user=True)
        if not client:
            raise HTTPException(401, detail="Unathorizated")
        password, salt = passwords.hash_password(info.password.encode("utf-8"))
        for key, value in info.model_dump().items():
            if key in ["name", "email", "gender", "location", "age"]:
                if value is None:
                    raise HTTPException(403)
                setattr(client, key, value)

        setattr(client, "hashed_pass", password)
        setattr(client, "salt", salt)

        await session.commit()

        return {
            "name": client.name,
            "email": client.email,
            "gender": client.gender,
            "location": client.location,
            "age": client.age
        }

@router.post("/clients/login")
async def login_clients(info: schemas.ClientsLogin, session: AsyncSession = Depends(database.db_get)):
    async with session.begin():
        client = await database.query(session, models.Client, [models.Client.email == info.email])
        if not client or not passwords.check_password(client.hashed_pass, info.password.encode("utf-8"), client.salt):
            raise HTTPException(401, detail="Unauthorized")
        token = jwt.create_jwt({"id": str(client.id)})

    return {
        "token":token
    }

@router.get("/clients/get_id")
async def get_id(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        client = await database.query(session, models.Client, [models.Client.id == user_data["id"]], user=True)
        expires = datetime.datetime.now(tz=timezone.utc) + timedelta(days=1)
        temp_id = jwt.create_jwt({"id": str(client.id), "exp": expires})
        return {
                "name": client.name,
                "token": temp_id
                }
    
@router.get("/clients/get_programs")
async def get_programs(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        client = await database.query(session, models.Client, [models.Client.id == user_data["id"]], user=True)
        progress = await database.query_bulk(session, models.LoyalProgramProgress, [models.LoyalProgramProgress.client_id == client.id])
        ids = []
        businesses = []
        points = []
        
        for entry in progress:
            ids.append(models.LoyalProgram.id == entry.loyal_id)
            points.append(entry.point_count)

        loyals = await database.query_bulk(session, models.LoyalProgram, [or_(*ids)])

        for entry in loyals:
            businesses.append(models.Business.id == entry.business_id)

        businesses = await database.query_bulk(session, models.Business, [or_(*businesses)])
        output = []

        for i in range(len(ids)):
            output.append({
                            "business_name": businesses[i].name,
                            "business_id": businesses[i].id,
                            "name": loyals[i].name,
                            "type": loyals[i].type,
                            "target": loyals[i].goal,
                            "reward": loyals[i].reward,
                            "points": points[i]
                        })

        return output