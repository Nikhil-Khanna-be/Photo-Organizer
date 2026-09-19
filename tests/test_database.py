from sqlalchemy import text
from src.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT DATABASE()"))
    database_name = result.scalar()

    print("Connected to database:", database_name)