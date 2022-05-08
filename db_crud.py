from sqlalchemy.future import select
from sqlalchemy.sql import func

import models
from database import SessionLocal


db = SessionLocal()


# Continent

async def create_continent(name, population, area_in_sqm):

    # waiting for 5 seconds to simulate heavy computation
    # sleep(5)
    print ("step 1 reached")

    continent_model = models.Continent()
    continent_model.name = name
    continent_model.population = population
    continent_model.area_in_sqm = area_in_sqm
    db.add(continent_model)
    await db.commit()

    return f"Continent - {name} has been created"

async def update_continent(continent_id, name, population, area_in_sqm):
    result = await db.execute(select(models.Continent).where(models.Continent.id == continent_id))
    continent_model = result.scalar_one_or_none()    
    if continent_model is None:
        ############## Handle this
        return "404 - Continent not found"
    
    continent_model.name = name
    continent_model.population = population
    continent_model.area_in_sqm = area_in_sqm

    db.add(continent_model)
    await db.commit()

    return f"Continent - {name} has been updated"

async def delete_continent(continent_id):
    result = await db.execute(select(models.Continent).where(models.Continent.id == continent_id))
    continent_model = result.scalar_one_or_none()    
    if continent_model is None:
        return "404 - Continent not found"
    
    await db.delete(continent_model)

    db.commit()

    return f"Continent - {continent_model.name} has been deleted"


# Country

async def create_country(name, population, area_in_sqm, quantity_hospitals, quantity_national_parks, continent_name):
    country_model = models.Country()
    result = await db.execute(select(models.Continent).where(models.Continent.name == continent_name))
    continent = result.scalar_one_or_none()
    if continent is None:
        return "Continent does not exist"

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

    country_model.name = name
    
    if population > continent.population - sum_country_population:
        return "Population input is wrong"
    country_model.population = population
    if area_in_sqm > continent.area_in_sqm - sum_country_area:
        return "Area input is wrong"
    country_model.area_in_sqm = area_in_sqm
    country_model.quantity_hospitals = quantity_hospitals
    country_model.quantity_national_parks = quantity_national_parks
    country_model.continent = continent

    # Null continent_id is added if continent does not exist. Assuming continents would be added first.

    db.add(country_model)
    await db.commit()

    return f"Country - {name} has been created"

async def update_country(country_id, name, population, area_in_sqm, quantity_hospitals, quantity_national_parks, continent_name):
    result1 = await db.execute(select(models.Country).where(models.Country.id == country_id))
    country_model = result1.scalar_one_or_none()    
    if country_model is None:
        return "Country does not exist"
    
    result2 = await db.execute(select(models.Continent).where(models.Continent.name == continent_name))
    continent = result2.scalar_one_or_none()
    if continent is None:
        return "Continent does not exist"

      # calculate sum
    q1 = await db.execute(select(func.sum(models.Country.area_in_sqm)).where(models.Country.continent_id == continent.id))
    sum_country_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.Country.population)).where(models.Country.continent_id == continent.id))
    sum_country_population = q2.scalar_one_or_none()

    if sum_country_population is None:
        sum_country_population = 0
    if sum_country_area is None:    
        sum_country_area = 0

    country_model.name = name
    if population > continent.population - (sum_country_population - country_model.population):
        return "Population input is wrong"
    country_model.population = population
    if area_in_sqm > continent.area_in_sqm - (sum_country_area - country_model.area_in_sqm):
        return "Area input is wrong"
    country_model.area_in_sqm = area_in_sqm
    country_model.quantity_hospitals = quantity_hospitals
    country_model.quantity_national_parks = quantity_national_parks
    country_model.continent = continent

    db.add(country_model)
    await db.commit()

    return f"Country - {name} has been updated"

async def delete_country(country_id):
    result = await db.execute(select(models.Country).where(models.Country.id == country_id))
    country_model = result.scalar_one_or_none() 
    if country_model is None:
        return "Country not found"
    
    await db.delete(country_model)
    db.commit()

    return f"Country - {country_model.name} has been deleted"


# City

async def create_city(name, population, area_in_sqm, quantity_trees, quantity_roads, country_name):
    city_model = models.City()

    result = await db.execute(select(models.Country).where(models.Country.name == country_name))
    country = result.scalar_one_or_none()
    if country is None:
        return "Country does not exist"

    # calculate sum
    q1 = await db.execute(select(func.sum(models.City.area_in_sqm)).where(models.City.country_id == country.id))
    sum_city_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.City.population)).where(models.City.country_id == country.id))
    sum_city_population = q2.scalar_one_or_none()
    if sum_city_population is None:
        sum_city_population = 0
    if sum_city_area is None:
        sum_city_area = 0

    city_model.name = name
    if population > country.population - sum_city_population:
        return "Population input is wrong"
    city_model.population = population
    if area_in_sqm > country.area_in_sqm - sum_city_area:
        return "Area input is wrong"
    city_model.area_in_sqm = area_in_sqm
    city_model.quantity_trees = quantity_trees
    city_model.quantity_roads = quantity_roads
    city_model.country = country

    db.add(city_model)
    await db.commit()

    return f"City - {name} has been created"

async def update_city(city_id, name, population, area_in_sqm, quantity_trees, quantity_roads, country_name):
    result1 = await db.execute(select(models.City).where(models.City.id == city_id))
    city_model = result1.scalar_one_or_none()    
    if city_model is None:
        return"City does not exist"
    
    result2 = await db.execute(select(models.Country).where(models.Country.name == country_name))
    country = result2.scalar_one_or_none()
    if country is None:
        return "Country does not exist"

      # calculate sum
    q1 = await db.execute(select(func.sum(models.City.area_in_sqm)).where(models.City.country_id == country.id))
    sum_city_area= q1.scalar_one_or_none()
    q2 = await db.execute(select(func.sum(models.City.population)).where(models.City.country_id == country.id))
    sum_city_population = q2.scalar_one_or_none()

    if sum_city_population is None:
        sum_city_population = 0
    if sum_city_area is None:
        sum_city_area = 0

    city_model.name = name
    if population > country.population - (sum_city_population - city_model.population):
        return "Population input is wrong"
    city_model.population = population
    if area_in_sqm > country.area_in_sqm - (sum_city_area - city_model.area_in_sqm):
        return "Area input is wrong"
    city_model.area_in_sqm = area_in_sqm
    city_model.quantity_trees = quantity_trees
    city_model.quantity_roads = quantity_roads
    city_model.country = country

    db.add(city_model)
    await db.commit()

    return f"City - {name} has been updated"

async def delete_city(city_id):
    result = await db.execute(select(models.City).where(models.City.id == city_id))
    city_model = result.scalar_one_or_none() 
    if city_model is None:
        return "City not found"

    await db.delete(city_model)
    db.commit()

    return f"City - {city_model.name} has been deleted"
