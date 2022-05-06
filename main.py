# from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from pydantic import BaseModel, validator

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



#Continent CRUD
class Continent(BaseModel):
    name: str 
    population: int 
    area_in_sqm: int 

@app.get("/continent")
async def get_all_continents(db: Session = Depends(get_db)):
    return db.query(models.Continent).all()


@app.get("/continent/{continent_id}")
async def get_continent_by_id(continent_id: int, db: Session = Depends(get_db)):
    continent_model = db.query(models.Continent).filter(models.Continent.id == continent_id).first()

    if continent_model is not None:
        return continent_model
    raise http_exception(404, "Item not found")


@app.post("/continent")
async def create_continent(continent: Continent, db: Session = Depends(get_db)):
    continent_model = models.Continent()
    continent_model.name = continent.name.capitalize()
    continent_model.population = continent.population
    continent_model.area_in_sqm = continent.area_in_sqm

    db.add(continent_model)
    db.commit()

    return succesful_response(201)

@app.put("/continent/{continent_id}")
async def update_continent(continent_id: int, continent: Continent, db: Session = Depends(get_db)):
    continent_model = db.query(models.Continent).filter(models.Continent.id == continent_id).first()
    
    if continent_model is None:
        raise http_exception(404, "Item not found")
    
    continent_model.name = continent.name.capitalize()
    continent_model.population = continent.population
    continent_model.area_in_sqm = continent.area_in_sqm

    db.add(continent_model)
    db.commit()

    return succesful_response(200)

@app.delete("/continent/{continent_id}")
async def delete_continent(continent_id: int, db: Session = Depends(get_db)):
    continent_model = db.query(models.Continent).filter(models.Continent.id == continent_id).first()
    
    if continent_model is None:
        raise http_exception(404, "Item not found")
    
    db.query(models.Continent).filter(models.Continent.id == continent_id).delete()

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
async def get_all_countries(db: Session = Depends(get_db)):
    return db.query(models.Country).all()

@app.get("/country/{country_id}")
async def get_country_by_id(country_id: int, db: Session = Depends(get_db)):
    country_model = db.query(models.Country).filter(models.Country.id == country_id).first()

    if country_model is not None:
        return country_model
    raise http_exception(404, "Item not found")

@app.post("/country")
async def create_country(country: Country, db: Session = Depends(get_db)):
    country_model = models.Country()
    # await db.connection()
    continent = db.query(models.Continent).filter_by(name=country.continent.capitalize()).first()

    continent_population = continent.population
    print(continent.population, continent.area_in_sqm, type(continent.population), continent_population)


      # calculate sum
    sum_country = db.query(func.sum(models.Country.area_in_sqm), func.sum(models.Country.population)).filter(models.Country.continent_id == continent.id).all()
    sum_country_area = sum_country[0][0]
    sum_country_population = sum_country[0][1]

    country_model.name = country.name.capitalize()
    # if country.population > continent_population - sum_country_population:
    #     raise http_exception(400, "Bad Population Input")
    country_model.population = country.population
    # if country.area_in_sqm > continent.area_in_sqm - sum_country_area:
    #     raise http_exception(400, "Bad Area Input")
    country_model.area_in_sqm = country.area_in_sqm
    country_model.quantity_hospitals = country.quantity_hospitals
    country_model.quantity_national_parks = country.quantity_national_parks
    country_model.continent = continent

    # print(sum_country_area, continent.area_in_sqm, sum_country_area[0][0], sum_country_area[0][1])
    # Null continent_id is added if continent does not exist. Assuming continents would be added first.

    db.add(country_model)
    db.commit()

    return succesful_response(201)

@app.put("/country/{country_id}")
async def update_country(country_id: int, country: Country, db: Session = Depends(get_db)):
    country_model = db.query(models.Country).filter(models.Country.id == country_id).first()
    if country_model is None:
        raise http_exception()
    
    continent = db.query(models.Continent).filter_by(name=country.continent.capitalize()).first()

      # calculate sum
    sum_country = db.query(func.sum(models.Country.area_in_sqm), func.sum(models.Country.population)).filter(models.Country.continent_id == continent.id).all()
    sum_country_area = sum_country[0][0]
    sum_country_population = sum_country[0][1]

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
    db.commit()

    return succesful_response(200)

@app.delete("/country/{country_id}")
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country_model = db.query(models.Country).filter(models.Country.id == country_id).first()
    
    if country_model is None:
        raise http_exception()
    
    db.query(models.Country).filter(models.Country.id == country_id).delete()
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
async def get_all_cities(db: Session = Depends(get_db)):
    return db.query(models.City).all()


@app.post("/city")
async def create_city(city: City, db: Session = Depends(get_db)):
    city_model = models.City()
    country = db.query(models.Country).filter_by(name=city.country.capitalize()).first()

      # calculate sum
    sum_city = db.query(func.sum(models.City.area_in_sqm), func.sum(models.City.population)).filter(models.City.country_id == country.id).all()
    sum_city_area = sum_city[0][0]
    sum_city_population = sum_city[0][1]

    print(sum_city, sum_city[0][0], sum_city[0][1])



    city_model.name = city.name
    # if city.population > country.population - sum_city_population:
    #     raise http_exception(400, "Bad Population Input")
    city_model.population = city.population
    # if city.area_in_sqm > country.area_in_sqm - sum_city_area:
    #     raise http_exception(400, "Bad Area Input")
    city_model.area_in_sqm = city.area_in_sqm
    city_model.quantity_trees = city.quantity_trees
    city_model.quantity_roads = city.quantity_roads
    city_model.continent = country


    db.add(city_model)
    db.commit()

    return succesful_response(201)

def succesful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'succesful'
    }

def http_exception(code: int, desc : str):
    return HTTPException(status_code=code, detail=desc)
