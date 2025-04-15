from fastapi import APIRouter, Depends, HTTPException, Body, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from src import jwt, passwords, database, models, schemas, images
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID as uuid4

router = APIRouter(tags=["Business"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/business/login")

max_file_size = 10 * 1024 * 1024

def file_allowed(extension):
    return extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']

@router.post("/business/register", status_code=201)
async def register_business(info: schemas.BusinessAdd, session: AsyncSession = Depends(database.db_get)):
    async with session.begin():
        query = await database.query(session, models.Business, [models.Business.email == info.email], True)
        if query:
            raise HTTPException(409, detail="Conflict")

        password, salt = passwords.hash_password(info.password.encode("utf-8"))
        db_item = models.Business(
            name=info.name,
            description=info.description,
            location=info.location,
            email=info.email,
            hashed_pass=password,
            salt=salt
        )
        session.add(db_item)
        await session.flush()

    await session.refresh(db_item)
    token = jwt.create_jwt({"id": str(db_item.id), "name": db_item.name})

    return {
        "id": str(db_item.id),
        "token": token
    }

@router.post("/business/login")
async def login_business(info: schemas.BusinessLogin, session: AsyncSession = Depends(database.db_get)):
    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.email == info.email], True, True)
        if not business or not passwords.check_password(business.hashed_pass, info.password.encode("utf-8"), business.salt):
            raise HTTPException(401, detail="Unauthorized")
        token = jwt.create_jwt({"id": str(business.id), "name": business.name})

    return {
        "token": token
    }

@router.get("/business/info")
async def info_business(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == user_data["id"]], user=True)

        return {
            "id": business.id,
            "email": business.email,
            "name": business.name,
            "description": business.description,
            "location": business.location
        }
    
@router.patch("/business/info")
async def edit_business(info: schemas.BusinessEdit, token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == user_data["id"]], False)
        if not business:
            raise HTTPException(401, detail="Unathorizated")
        business = await database.query(session, models.Business, [models.Business.id == user_data["id"]], user=True)
        for key, value in info.model_dump().items():
            if key in ["email", "password", "name", "description", "location"]:
                if value is None:
                    continue
                if key == "password":
                    password, salt = passwords.hash_password(value.encode("utf-8"))
                    setattr(business, "hashed_pass", password)
                    setattr(business, "salt", salt)
                    continue
                setattr(business, key, value)

        await session.commit()

        return {
            "id": business.id,
            "email": business.email,
            "name": business.name,
            "description": business.description,
            "location": business.location
        }

@router.post("/business/info/image")
async def upload_image(token: Annotated[str, Depends(oauth2_scheme)], file: UploadFile = File(...), session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == user_data["id"]], False, True)
        extension = file.filename.split('.')[-1]
              
        if not file_allowed(extension):
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        file = await file.read()

        if len(file) > max_file_size:
            raise HTTPException(status_code=400, detail="File is too large")
        
        path = f"/images/{business.id}.{extension}"
        business.image = path
        await session.commit()
        await images.upload_image(file, path)
        
        return {"image_id": business.id}
    
@router.get("/business/{id}/image")
async def get_image(id: uuid4, session: AsyncSession = Depends(database.db_get)):
    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == id], True)
        if not business or not business.image:
            return await images.default_image()
        return await images.download_image(business.image)

@router.get("/business/programs")
async def get_programs(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(token)
    async with session.begin():
        business = await database.query(session, models.Business, [models.Business.id == user_data["id"]], user=True)
        programs = await database.query_bulk(session, models.LoyalProgram, [models.LoyalProgram.business_id == business.id])
        output = []
        for entry in programs:
            output.append({
                            "id": str(entry.id),
                            "name": entry.name,
                            "target": entry.goal,
                            "reward": entry.reward,
                            "max_claims": entry.max_activations
                        })
            
        return output
    
@router.post("/business/check_id")
async def info_client_id(auth_token: Annotated[str, Depends(oauth2_scheme)], token: Annotated[str, Body(embed=True)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(auth_token)
    client_data = jwt.decode_jwt(token)

    async with session.begin():
        user = await database.query(session, models.Business, [models.Business.id == user_data["id"]], user=True)
        
        client = await database.query(session, models.Client, [models.Client.id == client_data["id"]], user=True)

        loyal = await database.query(session, models.LoyalProgram, [models.LoyalProgram.business_id == user.id], True)

        if not loyal:  
            raise HTTPException(403)

        loyal_progress = await database.query(session, models.LoyalProgramProgress, [models.LoyalProgramProgress.client_id == client_data["id"]], True)

        if loyal_progress == None:
            stat = await database.query(session, models.LoyalProgramStats, [models.LoyalProgramStats.id == loyal.id])

            loyal_progress = models.LoyalProgramProgress(
                loyal_id = loyal.id,
                client_id = client.id,
                reward_count = 0,
                point_count = 0
            )

            stat.total_clients += 1
            
            if client.gender != None:
                if client.gender == "male":
                    stat.male_count += 1
                if client.gender == "female":
                    stat.female_count += 1

            if client.age != None:
                if client.age < 18:
                    stat.children += 1
                if 18 <= client.age < 30:
                    stat.youngsters += 1
                if 30 < client.age <= 50:
                    stat.middle_aged += 1
                if 50 < client.age <= 70:
                    stat.old += 1
                if client.age > 70:
                    stat.very_old += 1

            session.add(loyal_progress)
            await session.commit()

        if loyal.business_id != user.id:
            raise HTTPException(status_code=403)
        
        return {
            "name": loyal.name,
            "type": loyal.type,
            "target": loyal.goal,
            "redeemable": client.name != None,
            "reward": loyal.reward,
            "points": loyal_progress.point_count
        }

@router.post("/business/redeem_id", status_code=204)
async def redeem_client_id(auth_token: Annotated[str, Depends(oauth2_scheme)], token: Annotated[str, Body(embed=True)], session: AsyncSession = Depends(database.db_get)):
    user_data = jwt.decode_jwt(auth_token)
    client_data = jwt.decode_jwt(token) 
    
    async with session.begin():
        user = await database.query(session, models.Business, [models.Business.id == user_data["id"]], user=True)
         
        client = await database.query(session, models.Client, [models.Client.id == client_data["id"]], user=True)

        loyal = await database.query(session, models.LoyalProgram, [models.LoyalProgram.business_id == user.id], True)

        loyal_progress = await database.query(session, models.LoyalProgramProgress, [models.LoyalProgramProgress.client_id == client.id])

        if loyal.business_id != user.id or not loyal_progress or not loyal:
            raise HTTPException(403)
        
        stat = await database.query(session, models.LoyalProgramStats, [models.LoyalProgramStats.id == loyal.id])

        if loyal.type == "reward":
            if loyal_progress.point_count == loyal.goal:
                loyal_progress.point_count = 0
                loyal_progress.reward_count += 1
                stat.total_rewarded += 1
                if client.name is None:
                    raise HTTPException(403)
                if loyal_progress.reward_count <= loyal.max_activations:
                    return
                elif loyal_progress.reward_count > loyal.max_activations:
                    raise HTTPException(403)
            else:
                loyal_progress.point_count += loyal.points_per_activation
                stat.total_points += loyal.points_per_activation
                return
            
        elif loyal.type == "discount":
            if loyal_progress.point_count >= loyal.goal:
                return
            else:
                loyal_progress.point_count += loyal.points_per_activation
                stat.total_points += loyal.points_per_activation
                return