# from uuid import UUID

from fastapi import FastAPI, Depends
import models
from database import SessionLocal, engine, Base
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field
import celery_worker

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
        await session.commit()

@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

#Continent CRUD
class Continent(BaseModel):
    name: str 
    population: int = Field(gt=0)
    area_in_sqm: int = Field(gt=0)

@app.get("/continent")
async def get_all_continents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Continent))
    return result.scalars().all()


@app.post("/continent")
async def post_continent(continent: Continent):

    task_id = celery_worker.create_continent.delay(continent.name.title(), continent.population, continent.area_in_sqm)
    return {"message": f"{continent.name.title()} has been received for creation",
            "task_id": f"{task_id}"}


@app.put("/continent/{continent_id}")
async def put_continent(continent_id: int, continent: Continent):
    
    task_id = celery_worker.update_continent.delay(continent_id, continent.name.title(), continent.population, continent.area_in_sqm)
    
    return {"message": f"{continent.name.title()} has been received for updation",
            "task_id": f"{task_id}"}


@app.delete("/continent/{continent_id}")
async def delete_continent(continent_id: int):
    
    task_id = celery_worker.delete_continent.delay(continent_id)

    return {"message": f"Continent with id - {continent_id} has been received for deletion",
            "task_id": f"{task_id}"}

#Country CRUD

class Country(BaseModel):
    name: str 
    population: int = Field(gt=0)
    area_in_sqm: int = Field(gt=0)
    quantity_national_parks: int = Field(gt=0)
    quantity_hospitals: int = Field(gt=0)
    continent: str

@app.get("/country")
async def get_all_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country))
    return result.scalars().all()


@app.post("/country")
async def create_country(country: Country):
    task_id = celery_worker.create_country.delay(country.name.title(), country.population, country.area_in_sqm, country.quantity_hospitals, country.quantity_national_parks, country.continent.title())

    return {"message": f"{country.name.title()} has been received for creation",
            "task_id": f"{task_id}"}

@app.put("/country/{country_id}")
async def update_country(country_id: int, country: Country):
    task_id = celery_worker.update_country.delay(country_id, country.name.title(), country.population, country.area_in_sqm, country.quantity_hospitals, country.quantity_national_parks, country.continent.title())

    return {"message": f"{country.name.title()} has been received for updation",
            "task_id": f"{task_id}"}

@app.delete("/country/{country_id}")
async def delete_country(country_id: int):
    task_id = celery_worker.delete_country.delay(country_id)

    return {"message": f"Country with id - {country_id} has been received for deletion",
            "task_id": f"{task_id}"}


# City CRUD

class City(BaseModel):
    name: str 
    population: int = Field(gt=0)
    area_in_sqm: int = Field(gt=0)
    quantity_trees: int = Field(gt=0)
    quantity_roads: int = Field(gt=0)
    country: str

@app.get("/city")
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.City))
    return result.scalars().all()

@app.post("/city")
async def create_city(city: City):
    task_id = celery_worker.create_city.delay(city.name.title(), city.population, city.area_in_sqm, city.quantity_trees, city.quantity_roads, city.country.title())

    return {"message": f"{city.name.title()} has been received for creation",
            "task_id": f"{task_id}"}

@app.put("/city/{city_id}")
async def update_city(city_id: int, city: City):
    task_id = celery_worker.update_city.delay(city_id, city.name.title(), city.population, city.area_in_sqm, city.quantity_trees, city.quantity_roads, city.country.title())

    return {"message": f"{city.name.title()} has been received for updation",
            "task_id": f"{task_id}"}


@app.delete("/city/{city_id}")
async def delete_city(city_id: int):
    task_id = celery_worker.delete_city.delay(city_id)

    return {"message": f"City with id - {city_id} has been received for deletion",
            "task_id": f"{task_id}"}


def succesful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'succesful'
    }


