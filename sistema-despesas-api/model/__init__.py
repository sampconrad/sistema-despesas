import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from model.base import Base
from model.despesa import Despesa, TipoDespesa

db_path = "database/"
if not os.path.exists(db_path):
   os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url) 

Base.metadata.create_all(engine)
