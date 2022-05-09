## Run the application 

clone this repository and run `docker-compose up`

This will start a fastapi application, a RabbitMQ server and a Celery worker, with a sqlite database. 
Open the fastapi openapi Swagger UI - specification which works as our client in this project. - 

http://127.0.0.1:8000/docs


## Validation checks -

Continent population and area_in_sqm should be greater than the sum of all countries in it. Similarly, Country population and area should be greater than the sum of all cities in it.

I had initially thought to do the validation at the pydantic model level, rather than adding validation to each api. But doing so with the pydantic validator is not recommended.
as mentioned here:

https://github.com/samuelcolvin/pydantic/issues/1227 
https://github.com/tiangolo/fastapi/issues/979

You shouldn't do IO (including db access) in validators, because:

- most new development would use asyncio for db access which won't work in validators which aren't coroutines
- it's very useful to have a hard distinction between checking the data integrity and checking whether it's consistent with the rest of the world (Pydantic models are used for checking data Integrity primarily)

Thus, I'll have to do the validation at each api.

I did so by using AsyncSession of SQLAlchemy, and awaiting db calls. Thus before adding any update or create to the database, the worker does a sanity check with the db i.e the source of truth.

## Client and Message broker services - 

I used fastapi as my client, which sends request to the celery worker through a RabbitMQ message broker. Celery has good python support and is easy to queue tasks in the message broker -RabbitMQ by the use of a delay() call option.

## Production - 

To run this in production. I would use:

- Postgres as my database as it is more robust. 
- Alembic for database migrations in case i need to make any changes in the db. 
- The client, message broker and the database run on the same computer/server rn. I would put them in different servers for seperation of concerns. 
- I would add Authentication/authorization through the use of some authorization protocool eg OAuth and also add CORS policies

