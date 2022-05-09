from celery import Celery
from celery.utils.log import get_task_logger

import asyncio
import db_crud



# Initialize Celery
celery = Celery('tasks', broker = 'amqp://guest:guest@rabbitmq-server:5672//')

# Create logger - display messages on task logger
celery_log = get_task_logger(__name__)

#Continent
@celery.task
def create_continent(name, population, area_in_sqm):
    result = asyncio.run(db_crud.create_continent(name, population, area_in_sqm))

    # Display log    
    # celery_log.info(f"Continent Created")
    return {"message": f"{result}"}

@celery.task
def update_continent(continent_id, name, population, area_in_sqm):
    result = asyncio.run(db_crud.update_continent(continent_id, name, population, area_in_sqm))

    return {"message": f"{result}"}

@celery.task
def delete_continent(continent_id):
    result = asyncio.run(db_crud.delete_continent(continent_id))

    return {"message": f"{result}"}

#Country
@celery.task
def create_country(name, population, area_in_sqm, quantity_hospitals, quantity_national_parks, continent_name):
    result = asyncio.run(db_crud.create_country(name, population, area_in_sqm, quantity_hospitals, quantity_national_parks, continent_name))

    return {"message": f"{result}"}

@celery.task
def update_country(country_id, name, population, area_in_sqm, quantity_hospitals, quantity_national_parks, continent_name):
    result = asyncio.run(db_crud.update_country(country_id, name, population, area_in_sqm, quantity_hospitals, quantity_national_parks, continent_name))

    return {"message": f"{result}"}

@celery.task
def delete_country(country_id):
    result = asyncio.run(db_crud.delete_country(country_id))

    return {"message": f"{result}"}

#City
@celery.task
def create_city(name, population, area_in_sqm, quantity_trees, quantity_roads, country_name):
    result = asyncio.run(db_crud.create_city(name, population, area_in_sqm, quantity_trees, quantity_roads, country_name))

    return {"message": f"{result}"}

@celery.task
def update_city(city_id, name, population, area_in_sqm, quantity_trees, quantity_roads, country_name):
    result = asyncio.run(db_crud.update_city(city_id, name, population, area_in_sqm, quantity_trees, quantity_roads, country_name))

    return {"message": f"{result}"}

@celery.task
def delete_city(city_id):
    result = asyncio.run(db_crud.delete_city(city_id))

    return {"message": f"{result}"}

