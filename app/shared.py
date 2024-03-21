from random import random
from snowflake import SnowflakeGenerator

sf = SnowflakeGenerator(int(random() * 100))

def get_id() -> int:
    return next(sf)