One issue being faced is where to do data validation for area, and population. Since Continent population should be greater than the sum of all countries in it.

It is better to do the validation at the pydantic model level rather than adding validation to each api.
But doing so with the pydantic validator is not recommended

The short answer is you shouldn't do IO (including db access) in validators, because:

 - most new development would use asyncio for db access which won't work in validators which aren't coroutines
 - it's very useful to have a hard distinction between checking the data integrity and checking whether it's consistent with the rest of the world
 # https://github.com/samuelcolvin/pydantic/issues/1227
 # https://github.com/tiangolo/fastapi/issues/979

 so I'll have to do validation at the api level rn.