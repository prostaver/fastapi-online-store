import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

config = configparser.ConfigParser()

config.read(os.path.dirname(os.path.abspath(__file__)) + "/config.ini")
config.sections()

dbConfig = config["DATABASE"]

dbEngine, dbUser, dbPW, dbHost, dbPort, dbName = (
    dbConfig["ENGINE"],
    dbConfig["USER"],
    dbConfig["PASSWORD"],
    dbConfig["HOST"],
    dbConfig["PORT"],
    dbConfig["DBNAME"],
)

engine = create_engine(
    f"{dbEngine}://{dbUser}:{dbPW}@{dbHost}:{dbPort}/{dbName}", echo=True
)

DbSession = sessionmaker(bind=engine)


def get_db_connection():
    db = DbSession()
    try:
        yield db
    finally:
        db.close()
