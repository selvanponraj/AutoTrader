from datetime import datetime, date, timedelta
import time
import pandas as pd
import numpy as np
from intrinio_sdk.rest import ApiException
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import sessionmaker
from models import Company, Security, SecurityPrice, StockAdjustment, Exchange
import setup_psql_environment
import setup_intrinio_environment

BULK_API_CALL_LIMIT = 2


def get_all_exchanges(next_page=''):
    # https://docs.intrinio.com/documentation/python/get_all_stock_exchanges_v2

    page_size = 100
    try:
        api_response = stock_exchange_api.get_all_stock_exchanges(
            page_size=page_size)
    except ApiException as e:
        print("Exception: StockExchangeApi->get_all_stock_exchanges: %s\r\n" % e)
        return None

    return api_response


def get_all_securities(delisted='', next_page=''):
    # https://docs.intrinio.com/documentation/python/get_all_securities_v2

    active = True
    delisted = False
    currency = 'USD'
    composite_mic = 'USCOMP'
    next_page = next_page

    try:
        api_response = security_api.get_all_securities(
            active=active,
            delisted=delisted,
            currency=currency,
            composite_mic=composite_mic)
    except ApiException as e:
        print("Exception: SecurityApi->get_all_securities: %s\r\n" % e)
        return None

    return api_response


def get_security(identifier):
    # https://docs.intrinio.com/documentation/python/get_security_by_id_v2

    identifier = identifier

    try:
        api_response = security_api.get_security_by_id(identifier)
    except ApiException as e:
        print("Error trying to get data for ", identifier)
        print("Exception: SecurityApi->get_security_by_id: %s\r\n" % e)
        return None

    return api_response


def get_security_prices(identifier, start_date='', next_page=''):
    # https://docs.intrinio.com/documentation/python/get_security_stock_prices_v2

    start_date = start_date
    frequency = 'daily'
    page_size = 100

    if not start_date:
        page_size = 10000
    try:
        if (page_size <= 100):
            api_response = security_api.get_security_stock_prices(
                identifier,
                start_date=start_date,
                frequency=frequency,
                page_size=page_size,
                next_page=next_page)
        else:
            api_response = security_api.get_security_stock_prices(
                identifier,
                start_date=start_date,
                frequency=frequency,
                page_size=page_size,
                next_page=next_page)
            time.sleep(BULK_API_CALL_LIMIT)
    except ApiException as e:
        print("Exception: SecurityApi->get_security_historical_data: %s\n" % e)
        return None

    return api_response


def get_company(identifier):
    # https://docs.intrinio.com/documentation/python/get_company_v2

    identifier = identifier
    try:
        api_response = company_api.get_company(identifier)
    except ApiException as e:
        print("Exception: CompanyApi->get_company: %s\r\n" % e)
        return None

    return api_response


# Setup environment and create a session
db = setup_psql_environment.get_database()
Session = sessionmaker(bind=db)
session = Session()
intrinio_sdk = setup_intrinio_environment.get_connection()
production = setup_intrinio_environment.using_production()

# If production, add SP500 securities not already in database
# If sandbox, add all securities available not in database
query = session.query(Security).statement
existing_securities = pd.read_sql(query, db, index_col='id')
security_api = intrinio_sdk.SecurityApi()
company_api = intrinio_sdk.CompanyApi()

if production:
    # Get S&P500 constituents
    sp500_constituents = pd.read_csv("sp500_constituents.csv",
                                     dtype={'cik': object})
    securities_to_add = sp500_constituents[~sp500_constituents['ticker']
        .isin(existing_securities['ticker'])]

    # Lookup and compare ticker to company name.
    missing_securities = []
    strings_to_remove = ['limited', 'ltd', 'incorporated', 'inc', '.']
    for index, sp500_constituent in securities_to_add.iterrows():
        sp500_constituent.replace(np.nan, '', inplace=True)
        name = sp500_constituent['name'].lower()
        ticker = sp500_constituent['ticker'].upper()
        cik = sp500_constituent['cik']

        if cik:
            try:
                api_response = company_api.search_companies(cik)
            except ApiException as e:
                print("Exception: CompanyApi->search_companies: %s\r\n" % e)
                continue

            if api_response:
                for company in api_response.companies:
                    if company.ticker and company.ticker.upper() == ticker:
                        name = company.name
                        break
        else:
            for string in strings_to_remove:
                name = name.replace(string, '')

        query = name + ' ' + ticker

        try:
            api_response = security_api.search_securities(query)
        except ApiException as e:
            print("Exception when calling CompanyApi->search_companies: %s\r\n" % e)
            continue

        if api_response:
            match_found = False
            for security in api_response.securities:
                if security.ticker and security.code == 'EQS' and security.ticker.upper() == ticker.upper():
                    match_found = True
                    api_response = get_security(security.id)
                    if api_response:
                        stock = Security(
                            id_intrinio=api_response.id,
                            code=api_response.code,
                            currency=api_response.currency,
                            ticker=api_response.ticker,
                            name=api_response.name,
                            figi=api_response.figi,
                            composite_figi=api_response.composite_figi,
                            share_class_figi=api_response.share_class_figi
                        )
                        print("Adding security {name} with ticker: {ticker}."
                              .format(name=stock.name, ticker=stock.ticker))

                        session.add(stock)
                        session.commit()
                    break
            if not match_found:
                print("\nNo match found for query: {query}\n"
                      .format(query=query))
                missing_securities.append(query)

        else:
            print("No API response for: ", query)
            missing_securities.append(query)
    print('There were {length} missing securities. Trying search with larger page size.'
          .format(length=len(missing_securities)))

    for query in missing_securities:
        try:
            api_response = security_api.search_securities(
                query,
                page_size=10000)
            time.sleep(BULK_API_CALL_LIMIT)
        except ApiException as e:
            print("Exception when calling CompanyApi->search_companies: %s\r\n" % e)
            continue

        if api_response:
            match_found = False
            for security in api_response.securities:
                if security.ticker and security.code == 'EQS' and security.ticker.upper() == ticker.upper():
                    match_found = True
                    api_response = get_security(security.id)
                    if api_response:
                        stock = Security(
                            id_intrinio=api_response.id,
                            code=api_response.code,
                            currency=api_response.currency,
                            ticker=api_response.ticker,
                            name=api_response.name,
                            figi=api_response.figi,
                            composite_figi=api_response.composite_figi,
                            share_class_figi=api_response.share_class_figi
                        )
                        print(query)
                        print("Adding security {name} with ticker: {ticker}.\n"
                              .format(name=stock.name, ticker=stock.ticker))
                        session.add(stock)
                        session.commit()
                    break
            if not match_found:
                print("A match was not found for query: ", query)

        else:
            print("NO API RESPONSE FOR: ", query)

else:
    api_response = get_all_securities()
    new_securities = pd.DataFrame(api_response.securities_dict)
    while api_response.next_page:
        api_response = get_all_securities(api_response.next_page)
        page = pd.DataFrame(api_response.securities_dict)
        pd.concat([new_securities, page])

    columns = ['id', 'code', 'currency', 'ticker', 'name', 'figi',
               'composite_figi', 'share_class_figi']
    new_securities = new_securities[columns]
    new_securities.rename(columns={'id': 'id_intrinio'}, inplace=True)
    securities_to_add = new_securities[~new_securities['figi']
        .isin(existing_securities['figi'])]

    if len(securities_to_add) > 0:
        print("Adding {security_count} securities."
              .format(security_count=len(securities_to_add)))
        session.bulk_insert_mappings(Security, securities_to_add
                                     .to_dict(orient="records"))
        session.commit()
    else:
        print("No securities added.")

# Get Exchanges
stock_exchange_api = intrinio_sdk.StockExchangeApi()
api_response = get_all_exchanges()
exchanges = pd.DataFrame(api_response.stock_exchanges_dict)
while api_response.next_page:
    api_response = get_all_exchanges(api_response.next_page)
    page = pd.DataFrame(api_response.stock_exchanges_dict)
    pd.concat([exchanges, page])

exchanges.rename(columns={'id': 'id_intrinio'}, inplace=True)

query = session.query(Exchange).statement
existing_exchanges = pd.read_sql(query, db, index_col='id')
exchanges = exchanges[~exchanges['mic'].isin(existing_exchanges['mic'])]

if len(exchanges) > 0:
    print("Inserting {length} exchanges.".format(length=len(exchanges)))
    session.bulk_insert_mappings(Exchange, exchanges.to_dict(orient="records"))
    session.commit()
else:
    print("No exchanges added.")

# Update securities with exchange
securities = session.query(Security).outerjoin(Exchange).filter(Security.exchange_id is None)
if securities.count() > 0:
    query = session.query(Exchange).statement
    exchanges = pd.read_sql(query, db, index_col='id')
    for security in securities:
        api_response = get_security(security.id_intrinio)
        if api_response:
            security.exchange_id = int(exchanges[exchanges['mic'] ==
                                                 api_response.listing_exchange_mic].index[0])
    print("Updating {length} securities with an exchange."
          .format(length=securities.count()))
    session.commit()

# Get Companies
query = session.query(Security).outerjoin(Company).filter(and_(Company.security_id == None,
                                                               Security.has_missing_company.isnot(True))).statement
securities_without_company = pd.read_sql(query, db, index_col='id')

securities_without_company_data = []
for index, security in securities_without_company.iterrows():
    api_response = get_company(security.ticker)
    if not api_response:
        securities_without_company_data.append(security.ticker)
    else:
        company = Company(name=api_response.name,
                          cik=api_response.cik,
                          description=api_response.short_description[:2000]
                          if len(api_response.short_description) > 2000 else api_response.short_description,
                          company_url=api_response.company_url,
                          sic=api_response.sic,
                          employees=api_response.employees,
                          sector=api_response.sector,
                          industry_category=api_response.industry_category,
                          industry_group=api_response.industry_group,
                          security_id=index)
        print("Adding company {name}.".format(name=api_response.name))
        session.add(company)
        session.commit()
length = (len(securities_without_company) - len(securities_without_company_data))
print("Added {length} companies.".format(length=length))

if len(securities_without_company_data) > 0:
    securities_without_company = securities_without_company.loc[securities_without_company['ticker'].isin(securities_without_company_data)]
securities_without_company['has_missing_company'] = True
securities_without_company['id'] = securities_without_company.index
session.bulk_update_mappings(Security, securities_without_company.to_dict(orient="records"))
session.commit()
print("There were {rows} new rows that did not have an associated company record."
      .format(rows=len(securities_without_company_data)))

# Get Updated Prices
query = session.query(Security, func.max(SecurityPrice.date).label("latest_date")).outerjoin(SecurityPrice).group_by(Security.id).filter(Security.has_invalid_data.isnot(True)).statement
securities = pd.read_sql(query, db)
invalid_data_ids = []
for index, security in securities.iterrows():
    start_date = security.latest_date + timedelta(days=1) if security.latest_date else None
    api_response = get_security_prices(security.figi, start_date)
    if api_response:
        stock_prices = pd.DataFrame(api_response.stock_prices_dict)
        stock_prices['security_id'] = security.id
        while api_response.next_page:
            api_response = get_security_prices(security.figi, start_date, api_response.next_page)
            page = pd.DataFrame(api_response.stock_prices_dict)
            page['security_id'] = security.id
            pd.concat([stock_prices, page])

        stock_prices_to_add = stock_prices[~stock_prices.security_id.isin(invalid_data_ids)]
        stock_prices_to_add.replace({pd.np.nan: None}, inplace=True)

        if len(stock_prices_to_add) > 0:
            start_date = stock_prices_to_add['date'].min()
            end_date = stock_prices_to_add['date'].max()
            print("Ticker {ticker}: Adding {rows} rows to the security prices database with dates between {start_date} - {end_date}."
                .format(ticker=security.ticker, rows=len(stock_prices_to_add),
                start_date=start_date, end_date=end_date))
            session.bulk_insert_mappings(SecurityPrice, stock_prices_to_add.to_dict(orient="records"))
            session.commit()