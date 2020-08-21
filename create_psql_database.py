from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from setup_psql_environment import get_database
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db1


import models
import pandas as pd
# Setup environment and create a session
db = get_database()
Session = sessionmaker(bind=db)
meta = MetaData(bind=db)
session = Session()
company = db1.Table('company', meta, autoload=True, autoload_with=db)
connection = db.connect()
sql_df = pd.read_sql(
    "SELECT * FROM company",
    con=db,
    parse_dates=[
        'created_at',
        'updated_at'
    ]
)


# # Create database from SQLAlchemy models
models.Base.metadata.create_all(db)