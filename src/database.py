import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")


DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{MYSQL_USER}:{MYSQL_PASSWORD}@"
    f"{MYSQL_HOST}/{MYSQL_DATABASE}"
)

engine = create_engine(DATABASE_URL)