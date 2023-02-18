from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, "database.json")
secrets = json.loads(open(SECRET_FILE).read())
DB = secrets["DB"]

DB_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB["user"], DB["password"], DB["host"], DB["port"], DB["database"])

ENGINE = create_engine(DB_URL, encoding="utf-8", echo=True)
SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))
BASE = declarative_base()
BASE.query = SESSION.query_property()