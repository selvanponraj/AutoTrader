from faker import Faker

import time
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Column, Integer, String
from random import randint


msidns = [
    447810068040,
    447810067578,
    447810081030,
    447810068111,
    447810083444,
    447810082754
]

faker = Faker()

engine = create_engine('postgresql+psycopg2://alpha:alpha@localhost/alpha')
session = Session(engine)
metadata = MetaData(engine)
Base = automap_base()
# # Table - Uncomment below two lines.
Base.prepare(engine, reflect=True)

Subscription = Base.classes.subscription
Contact = Base.classes.contact
ModelScore = Base.classes.model_score
SubFlexAttribute = Base.classes.subs_flex_attribute
Account = Base.classes.account

# subscription = Table('subscription',Base.metadata, Column('subscription_id', String,
# primary_key=True), autoload=True, autoload_with=engine)
# Base.prepare(engine, reflect=True)
# Subscription = Base.classes.subscription

# v = Table('subscription_v', metadata, autoload=True)
# for r in engine.execute(subscription_v.select()):
#     print (r)


def clone_model(model, **kwargs):
    """Clone an arbitrary sqlalchemy model object without its primary key values."""
    # Ensure the model’s data is loaded before copying.
    # model.subscription_id
    table = model.__table__
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
    data = {c: getattr(model, c) for c in non_pk_columns}
    data.update(kwargs)
    clone = model.__class__(**data)
    return clone

''' 
    Documentation
    contact_id = 1-87-K5XXX  '  (X = last 3 digits of MSISDN)
    Subscription_id = 'TEST-100'(incremental)
    service_no = MSISDN
    root_service_product_cd = '100092'
    subs_type = 'Mobile Service',
    owner_acct_no, billing_acct_no, service_acct_no, account_no = allsame= 190041318  last 5 number is random
'''


def insert(table=None,start=None):
    t0 = time.time()

    sample_subscription = session.query(Subscription).filter(Subscription.service_no == '4475912234894')[0]
    print("subscription_id:", sample_subscription.service_no, sample_subscription.subscription_id)

    sample_ms = session.query(ModelScore).filter(ModelScore.service_no == '4475912234894')[0]
    print("model_id:", sample_ms.model_id, "model_name:", sample_ms.model_name)

    sample_contact = session.query(Contact).filter(Contact.contact_id == '1-87-K5484')[0]
    print("contact_id:", sample_contact.contact_birth_dt)

    sample_account = session.query(Account).filter(Account.account_no == '1900475484')[0]
    print("account_no:", sample_account.contact_id)

    sample_sfa = session.query(SubFlexAttribute).filter(SubFlexAttribute.subscription_id == '1-DE4894HJD')[0]
    print("sample_sfa:", sample_sfa.custom_char_003)

    for msidn in msidns:
        print(msidn)
        acct_no = "1900" + str(random_with_N_digits(5))
        # contact_id = "1-87-K5" + str(msidn)[len(str(msidn)) - 3:]
        contact_id = "1-87-K" + str(random_with_N_digits(4))

        subscription = clone_model(sample_subscription,
                                   subscription_id='TEST' + str(start + 1),
                                   service_no=str(msidn),
                                   subs_type='Mobile Service',
                                   # email_address=faker.email(),
                                   sms_mktg_consent_flg='N',
                                   root_service_product_cd = '100092',
                                   owner_acct_no=acct_no,
                                   billing_acct_no=acct_no,
                                   service_acct_no=acct_no)
        model_score = clone_model(sample_ms,
                                   model_id=5,
                                   service_no=str(msidn)
                                  )
        contact = clone_model(sample_contact,
                                   contact_id=contact_id
                              )
        account = clone_model(sample_account,
                                   account_no=acct_no,
                                   contact_id= contact_id
                                   )

        sample_sfa = clone_model(sample_sfa,
                              subscription_id='TEST' + str(start + 1),
                              custom_char_003=str(msidn)
                              )

        session.add(subscription)
        session.add(model_score)
        session.add(contact)
        session.add(account)
        session.add(sample_sfa)

        start = start + 1
        if start % 1000 == 0:
            session.flush()
    session.commit()
    print(
        "Total time for " + str(len(msidns)) +
        " records " + str(time.time() - t0) + " secs")


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def main():
    print("Test Data Preparation Subscription - Starting")
    insert(start=100)


if __name__=="__main__":
    main()



