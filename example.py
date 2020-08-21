from sqlalchemy import create_engine
import psycopg2 as pg
#load python script that batch loads pandas df to sql
from io import StringIO

address = 'postgresql://<username>:<pswd>@<host>:<port>/<database>'
engine = create_engine(address)
connection = engine.raw_connection()
cursor = connection.cursor()

#df is the dataframe containing an index and the columns "Event" and "Day"
#create Index column to use as primary key
df.reset_index(inplace=True)
df.rename(columns={'index':'Index'}, inplace =True)

#create the table but first drop if it already exists
command = '''DROP TABLE IF EXISTS localytics_app2;
CREATE TABLE localytics_app2
(
"Index" serial primary key,
"Event" text,
"Day" timestamp without time zone,
);'''
cursor.execute(command)
connection.commit()

#stream the data using 'to_csv' and StringIO(); then use sql's 'copy_from' function
output = StringIO.StringIO()
#ignore the index
df.to_csv(output, sep='\t', header=False, index=False)
#jump to start of stream
output.seek(0)
contents = output.getvalue()
cur = connection.cursor()
#null values become ''
cur.copy_from(output, 'localytics_app2', null="")
connection.commit()
cur.close()