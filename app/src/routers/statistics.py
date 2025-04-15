from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from src import models, schemas, database, jwt

router = APIRouter(tags=["Statistics"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/business/login")

@router.get("/statistics/business")
async def get_business_stats(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    business_data = jwt.decode_jwt(token)

    async with session.begin():
        stat = await database.query(session, models.LoyalProgramStats, [models.LoyalProgramStats.business_id == business_data["id"]])
        return {
                "total_rewarded": stat.total_rewarded,
                "total_points": stat.total_points,
                "total_clients": stat.total_clients,
                "male_count": stat.male_count,
                "female_count": stat.female_count,
                "children": stat.children,
                "youngsters": stat.youngsters,
                "middle_aged": stat.middle_aged,
                "old": stat.old,
                "very_old": stat.very_old
                }