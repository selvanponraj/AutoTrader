from faker import Faker

import time
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Column, Integer, String

faker = Faker()

engine = create_engine('postgresql+psycopg2://alpha:alpha@localhost/alpha')
session = Session(engine)
metadata = MetaData(engine)
Base = automap_base()
# Table - Uncomment below two lines.
# Base.prepare(engine, reflect=True)
# Subscription = Base.classes.subscription

subscription_v = Table('subscription_v',Base.metadata, Column('subscription_id', String,
primary_key=True), autoload=True, autoload_with=engine)
Base.prepare(engine, reflect=True)

# v = Table('subscription_v', metadata, autoload=True)
# for r in engine.execute(subscription_v.select()):
#     print (r)

Subscription = Base.classes.subscription_v


def clone_model(model, **kwargs):
    """Clone an arbitrary sqlalchemy model object without its primary key values."""
    # Ensure the model’s data is loaded before copying.
    model.subscription_id
    table = model.__table__
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
    data = {c: getattr(model, c) for c in non_pk_columns}
    data.update(kwargs)

    clone = model.__class__(**data)
    return clone


def test_sqlalchemy_orm_pk_given(start=0, end=2):
    t0 = time.time()
    msidn = 447000000000
    for i in range(start, start + end):
        msidn = msidn + 1
        print(msidn)
        subscription = clone_model(subscription_obj, subscription_id='-CATCH' + str(i + 1), service_no=str(msidn),
                                   email_address=faker.email())
        session.add(subscription)
        if i % 1000 == 0:
            session.flush()
    session.commit()
    print(
        "SQLAlchemy ORM pk given: Total time for " + str(end) +
        " records " + str(time.time() - t0) + " secs")


subscription_obj = session.query(Subscription).first()
test_sqlalchemy_orm_pk_given(200,20000)

# from random import randint
# def random_with_N_digits(n):
#     range_start = 10**(n-1)
#     range_end = (10**n)-1
#     return randint(range_start, range_end)
#
# for mciNumbers in range(0,5):
# 	print('447000000000', random_with_N_digits(7),'001')
