from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src import models, schemas, database, jwt
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID as uuid4
import uuid 

router = APIRouter(tags=["Programs"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/business/login")

@router.post("/programs/create", status_code=201)
async def create_program(token: Annotated[str, Depends(oauth2_scheme)], info: schemas.ProgramAdd, session: AsyncSession = Depends(database.db_get)):
    business_data = jwt.decode_jwt(token)

    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == business_data["id"]], user=True)

        id = uuid.uuid4()

        if info.type == "discount":
            if info.target > 100:    
                raise HTTPException(400, "Wrong goal for discount program")          

        db_item = models.LoyalProgram(
                            id = id,
                            business_id=business.id,
                            name=info.name,
                            type=str(info.type),
                            points_per_activation=info.points_per_activation,
                            goal=info.target,
                            reward=info.reward,
                            max_activations=info.max_claims
                        )  
                
        stat_item = models.LoyalProgramStats(
            id=id,
            business_id=business.id
        )

        session.add(db_item)
        session.add(stat_item)
        await session.flush()

        await session.refresh(db_item)

        return {
            "id": str(db_item.id),
            "type": db_item.type,
            "name": db_item.name,
            "target": db_item.goal,
            "reward": db_item.reward,
            "points_per_activation": db_item.points_per_activation,
            "max_claims": db_item.max_activations
        }

@router.patch("/programs/{id}")
async def edit_business(id: uuid4, info: schemas.ProgramEdit, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    business_data = jwt.decode_jwt(token)

    key_map = {
        "name": "name",
        "target": "goal",
        "reward": "reward",
        "max_claims": "max_activations",
        "points_per_activation": "points_per_activation"
    }

    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == business_data["id"]], user=True)

        program = await database.query(session, models.LoyalProgram, [models.LoyalProgram.id == id, models.LoyalProgram.business_id == business.id], True)

        if not program:
            raise HTTPException(404, detail="Not found")
        
        for key, value in info.model_dump().items():
            if key in ["name", "target", "reward", "max_claims", "points_per_activation"]:
                if value is None:
                    continue
                setattr(program, key_map[key], value)

        await session.commit()

        return {
            "id": str(program.id),
            "name": program.name,
            "type": program.type,
            "target": program.goal,
            "reward": program.reward,
            "points_per_activation": program.points_per_activation,
            "max_claims": program.max_activations
        }

@router.get("/programs/{id}")
async def get_business(id: uuid4, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    business_data = jwt.decode_jwt(token)

    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == business_data["id"]], user=True)

        program = await database.query(session, models.LoyalProgram, [models.LoyalProgram.id == id, models.LoyalProgram.business_id == business.id], True)

        if not program:
            raise HTTPException(404, detail="Not found")

        return {
            "id": str(program.id),
            "name": program.name,
            "type": program.type,
            "target": program.goal,
            "reward": program.reward,
            "points_per_activation": program.points_per_activation,
            "max_claims": program.max_activations
        }

@router.delete("/programs/{id}", status_code=204)
async def delete_business(id: uuid4, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    business_data = jwt.decode_jwt(token)

    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == business_data["id"]], user=True)

        program = await database.query(session, models.LoyalProgram, [models.LoyalProgram.id == id, models.LoyalProgram.business_id == business.id], True)

        if not program:
            raise HTTPException(404, detail="Not found")

        session.delete(program)

        await session.commit()
