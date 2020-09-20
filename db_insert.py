from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from setup_psql_environment import get_database
from sqlalchemy.ext.declarative import declarative_base
import models
import time
import random
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy import create_engine

# Setup environment and create a session

paym_msidns = list(map(str, [
    447810067578,
    447810081030,
    447876032230,
    447810068040,
    447810068111,
    447810083444,
    447810082754
]))
mbb_msidns = list(map(str, [
    447340011880,
    447810068835
]))
ssud_msidns = list(map(str, [
    447810068195,
    447810068123,
    447810067473,
    447810081030,
    447810010777
]))

# db = get_database()
db = create_engine('postgresql+psycopg2://alpha:alpha@localhost/alpha')
Session = sessionmaker(bind=db)


def delete(schema=None, type=None):

    meta = MetaData(schema=schema)
    Base = automap_base(bind=db, metadata=meta)
    Base.prepare(db, reflect=True)

    session = Session()

    Subscription = Base.classes.subscription
    Contact = Base.classes.contact
    ModelScore = Base.classes.model_score
    SubFlexAttribute = Base.classes.subs_flex_attribute
    Account = Base.classes.account

    if type == "PAYMS":
        msidns = paym_msidns
    if type == "MBB":
        msidns = mbb_msidns
    elif type == "SSUD":
        msidns = ssud_msidns
    else:
        msidns = paym_msidns + mbb_msidns + ssud_msidns

    session.query(Subscription).filter(Subscription.service_no.in_(msidns)).delete(synchronize_session='fetch')
    session.query(SubFlexAttribute).filter(SubFlexAttribute.custom_char_003.in_(msidns)).delete(synchronize_session='fetch')
    session.query(ModelScore).filter(ModelScore.service_no.in_(msidns)).delete(synchronize_session='fetch')
    contact_ids=session.query(Contact.contact_id).filter(Contact.alternate_phone_no.in_(msidns)).all()
    session.query(Account).filter(Account.contact_id.in_(contact_ids)).delete(synchronize_session='fetch')
    session.query(Contact).filter(Contact.alternate_phone_no.in_(msidns)).delete(synchronize_session='fetch')
    session.commit();

def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


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


def insert(schema=None, type=None):
    t0 = time.time()
    session = Session()
    print(session)
    meta = MetaData(schema=schema)
    Base = automap_base(bind=db, metadata=meta)
    Base.prepare(db, reflect=True)
    print(Base.classes.keys())
    print(Base.metadata.tables)

    Subscription = Base.classes.subscription
    Contact = Base.classes.contact
    ModelScore = Base.classes.model_score
    SubFlexAttribute = Base.classes.subs_flex_attribute
    Account = Base.classes.account

    sample_subscription = session.query(Subscription).filter(Subscription.service_no == '4475912234894')[0]
    print("subscription_id:", sample_subscription.service_no, sample_subscription.subscription_id)

    sample_sfa = session.query(SubFlexAttribute).filter(SubFlexAttribute.subscription_id == '1-DE4894HJD')[0]
    print("sample_sfa:", sample_sfa.custom_char_003)

    sample_contact = session.query(Contact).filter(Contact.contact_id == '1-87-K5484')[0]
    print("contact_id:", sample_contact.contact_birth_dt)

    sample_account = session.query(Account).filter(Account.account_no == '1900475484')[0]
    print("account_no:", sample_account.contact_id)

    sample_ms = session.query(ModelScore).filter(ModelScore.service_no == '4475912234894')[0]
    print("model_id:", sample_ms.model_id, "model_name:", sample_ms.model_name)

    subs_type = 'Mobile Service'
    root_service_product_cd = '100000'
    sms_mktg_consent_flg = 'N'

    if type == "PAYMS":
        msidns = paym_msidns
        subs_type = 'Mobile Service'
        root_service_product_cd = '100000'
        sms_mktg_consent_flg = 'N'
    if type == "MBB":
        msidns = mbb_msidns
        subs_type = 'Mobile Broadband Service'
        root_service_product_cd = '100092'
    elif type == "SSUD":
        msidns = ssud_msidns
        sms_mktg_consent_flg = 'Y'

    for msidn in msidns:
        print(msidn)
        subscription_id = 'T2S-TEST' + str(random_with_N_digits(7))
        acct_no = "1900" + str(random_with_N_digits(5))
        # contact_id = "1-87-K5" + str(msidn)[len(str(msidn)) - 3:]
        contact_id = "1-87-K" + str(random_with_N_digits(4))

        subscription = clone_model(sample_subscription,
                                   subscription_id=subscription_id,
                                   service_no=str(msidn),
                                   subs_type=subs_type,
                                   # email_address=faker.email(),
                                   sms_mktg_consent_flg=sms_mktg_consent_flg,
                                   root_service_product_cd=root_service_product_cd,
                                   owner_acct_no=acct_no,
                                   billing_acct_no=acct_no,
                                   service_acct_no=acct_no)
        model_score = clone_model(sample_ms,
                                  model_id=random_with_N_digits(4),
                                  service_no=str(msidn)
                                  )
        contact = clone_model(sample_contact,
                              contact_id=contact_id,
                              alternate_phone_no=str(msidn)
                              )
        account = clone_model(sample_account,
                              account_no=acct_no,
                              contact_id=contact_id
                              )

        sample_sfa = clone_model(sample_sfa,
                                 subscription_id=subscription_id,
                                 custom_char_003=str(msidn)
                                 )

        session.add(subscription)
        session.add(model_score)
        session.add(contact)
        session.add(account)
        session.add(sample_sfa)

        if len(msidns) % 1000 == 0:
            session.flush()
        session.commit()
        # session.close()
        print(
            "Total time for " + str(len(msidns)) +
            " records " + str(time.time() - t0) + " secs")


def main():
    print("Test Data Preparation  - Starting")

    # # ALPHADATA
    # insert(schema="alphadata", type="PAYMS")
    # insert(schema="alphadata", type="MBB")
    # insert(schema="alphadata", type="SSUD")

    #
    # # BETADATA
    # insert(schema="betadata",type="PAYMS")
    # insert(schema="betadata", type="MBB")
    # insert(schema="betadata", type="SSUD")

    delete(schema="betadata",type="PAYMS")

    # print(" ****************************** End of Test Data Preparation  ********************")


if __name__ == "__main__":
    main()
