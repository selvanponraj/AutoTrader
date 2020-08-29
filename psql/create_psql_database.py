from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from setup_psql_environment
from sqlalchemy.ext.declarative import declarative_base

import models

# Setup environment and create a session
db = get_database()
Session = sessionmaker(bind=db)
meta = MetaData(bind=db)
session = Session()

# Create database from SQLAlchemy models
models.Base.metadata.create_all(db)