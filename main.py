# from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
import models
from database import SessionLocal, engine, Base
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.future import select
from pydantic import BaseModel, validator

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
    population: int 
    area_in_sqm: int 

@app.get("/continent")
async def get_all_continents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Continent))
    return result.scalars().all()

@app.get("/continent/{continent_id}")
async def get_continent_by_id(continent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Continent).where(models.Continent.id == continent_id))
    continent_model = result.scalar_one_or_none()

    if continent_model is not None:
        return continent_model
    raise http_exception(404, "Item not found")

@app.post("/continent")
async def create_continent(continent: Continent, db: AsyncSession = Depends(get_db)):
    continent_model = models.Continent()
    continent_model.name = continent.name.capitalize()
    continent_model.population = continent.population
    continent_model.area_in_sqm = continent.area_in_sqm

    db.add(continent_model)
    await db.commit()

    return succesful_response(201)

@app.put("/continent/{continent_id}")
async def update_continent(continent_id: int, continent: Continent, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Continent).where(models.Continent.id == continent_id))
    continent_model = result.scalar_one_or_none()    
    if continent_model is None:
        raise http_exception(404, "Item not found")
    
    continent_model.name = continent.name.capitalize()
    continent_model.population = continent.population
    continent_model.area_in_sqm = continent.area_in_sqm

    db.add(continent_model)
    await db.commit()

    return succesful_response(200)

@app.delete("/continent/{continent_id}")
async def delete_continent(continent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Continent).where(models.Continent.id == continent_id))
    continent_model = result.scalar_one_or_none()    
    if continent_model is None:
        raise http_exception(404, "Item not found")
    
    await db.delete(continent_model)

    db.commit()

    return succesful_response(200)


#Country CRUD

class Country(BaseModel):
    name: str 
    population: int 
    area_in_sqm: int
    quantity_national_parks: int
    quantity_hospitals: int 
    continent: str

@app.get("/country")
async def get_all_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country))
    return result.scalars().all()

@app.get("/country/{country_id}")
async def get_country_by_id(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country).where(models.Country.id == country_id))
    country_model = result.scalar_one_or_none()

    if country_model is not None:
        return country_model
    raise http_exception(404, "Item not found")

@app.post("/country")
async def create_country(country: Country, db: AsyncSession = Depends(get_db)):
    country_model = models.Country()
    result = await db.execute(select(models.Continent).where(models.Continent.name == country.continent.capitalize()))
    continent = result.scalar_one_or_none()
    if continent is None:
        raise http_exception(400, "Continent does not exist")
    
    # print(continent.population, continent.area_in_sqm, type(continent.population))

    # calculate sum
    q1 = await db.execute(select(func.sum(models.Country.area_in_sqm)).where(models.Country.continent_id == continent.id))
    sum_country_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.Country.population)).where(models.Country.continent_id == continent.id))
    sum_country_population = q2.scalar_one_or_none()
    if sum_country_population is None:
        sum_country_population = 0
    if sum_country_area is None:    
        sum_country_area = 0

    country_model.name = country.name.capitalize()
    
    if country.population > continent.population - sum_country_population:
        raise http_exception(400, "Bad Population Input")
    country_model.population = country.population
    if country.area_in_sqm > continent.area_in_sqm - sum_country_area:
        raise http_exception(400, "Bad Area Input")
    country_model.area_in_sqm = country.area_in_sqm
    country_model.quantity_hospitals = country.quantity_hospitals
    country_model.quantity_national_parks = country.quantity_national_parks
    country_model.continent = continent

    # Null continent_id is added if continent does not exist. Assuming continents would be added first.

    db.add(country_model)
    await db.commit()

    return succesful_response(201)

@app.put("/country/{country_id}")
async def update_country(country_id: int, country: Country, db: AsyncSession = Depends(get_db)):
    result1 = await db.execute(select(models.Country).where(models.Country.id == country_id))
    country_model = result1.scalar_one_or_none()    
    if country_model is None:
        raise http_exception()
    
    result2 = await db.execute(select(models.Continent).where(models.Continent.name == country.continent.capitalize()))
    continent = result2.scalar_one_or_none()
    if continent is None:
        raise http_exception(400, "Continent does not exist")

      # calculate sum
    q1 = await db.execute(select(func.sum(models.Country.area_in_sqm)).where(models.Country.continent_id == continent.id))
    sum_country_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.Country.population)).where(models.Country.continent_id == continent.id))
    sum_country_population = q2.scalar_one_or_none()

    country_model.name = country.name.capitalize()
    #Since this is update, there already exists a population and area.
    if country.population > continent.population - (sum_country_population - country_model.population):
        raise http_exception(400, "Bad Population Input")
    country_model.population = country.population
    if country.area_in_sqm > continent.area_in_sqm - (sum_country_area - country_model.area_in_sqm):
        raise http_exception(400, "Bad Area Input")
    country_model.area_in_sqm = country.area_in_sqm
    country_model.quantity_hospitals = country.quantity_hospitals
    country_model.quantity_national_parks = country.quantity_national_parks
    country_model.continent = continent

    db.add(country_model)
    await db.commit()

    return succesful_response(200)

@app.delete("/country/{country_id}")
async def delete_country(country_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Country).where(models.Country.id == country_id))
    country_model = result.scalar_one_or_none() 
    if country_model is None:
        raise http_exception(404, "Item not found")
    
    await db.delete(country_model)
    db.commit()

    return succesful_response(200)


# City CRUD

class City(BaseModel):
    name: str 
    population: int 
    area_in_sqm: int
    quantity_roads: int
    quantity_trees: int 
    country: str

@app.get("/city")
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.City))
    return result.scalars().all()

@app.post("/city")
async def create_city(city: City, db: AsyncSession = Depends(get_db)):
    city_model = models.City()

    result = await db.execute(select(models.Country).where(models.Country.name == city.country.capitalize()))
    country = result.scalar_one_or_none()
    if country is None:
        raise http_exception(400, "Country does not exist")

    # calculate sum
    q1 = await db.execute(select(func.sum(models.City.area_in_sqm)).where(models.City.country_id == country.id))
    sum_city_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.City.population)).where(models.City.country_id == country.id))
    sum_city_population = q2.scalar_one_or_none()
    if sum_city_population is None:
        sum_city_population = 0
    if sum_city_area is None:
        sum_city_area = 0

    city_model.name = city.name
    if city.population > country.population - sum_city_population:
        raise http_exception(400, "Bad Population Input")
    city_model.population = city.population
    if city.area_in_sqm > country.area_in_sqm - sum_city_area:
        raise http_exception(400, "Bad Area Input")
    city_model.area_in_sqm = city.area_in_sqm
    city_model.quantity_trees = city.quantity_trees
    city_model.quantity_roads = city.quantity_roads
    city_model.country = country

    db.add(city_model)
    await db.commit()

    return succesful_response(201)

@app.put("/city/{city_id}")
async def update_city(city_id: int, city: City, db: AsyncSession = Depends(get_db)):
    result1 = await db.execute(select(models.City).where(models.City.id == city_id))
    city_model = result1.scalar_one_or_none()    
    if city_model is None:
        raise http_exception()
    
    result2 = await db.execute(select(models.Country).where(models.Country.name == city.country.capitalize()))
    country = result2.scalar_one_or_none()
    if country is None:
        raise http_exception(400, "Country does not exist")

      # calculate sum
    q1 = await db.execute(select(func.sum(models.City.area_in_sqm)).where(models.City.country_id == country.id))
    sum_city_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.City.population)).where(models.City.country_id == country.id))
    sum_city_population = q2.scalar_one_or_none()

    city_model.name = city.name.capitalize()
    #Since this is update, there already exists a population and area.
    if city.population > country.population - (sum_city_population - city_model.population):
        raise http_exception(400, "Bad Population Input")
    city_model.population = city.population
    if city.area_in_sqm > country.area_in_sqm - (sum_city_area - city_model.area_in_sqm):
        raise http_exception(400, "Bad Area Input")
    city_model.area_in_sqm = city.area_in_sqm
    city_model.quantity_trees = city.quantity_trees
    city_model.quantity_roads = city.quantity_roads
    city_model.country = country

    db.add(city_model)
    await db.commit()

    return succesful_response(200)

@app.delete("/city/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    city_model = result.scalar_one_or_none() 
    if city_model is None:
        raise http_exception(404, "Item not found")
    
    await db.delete(city_model)
    db.commit()

    return succesful_response(200)


def succesful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'succesful'
    }

def http_exception(code: int, desc : str):
    return HTTPException(status_code=code, detail=desc)
