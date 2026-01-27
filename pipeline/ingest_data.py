#!/usr/bin/env python
# coding: utf-8

import pandas as pd

year = 2021
month = 1

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz')


# In[8]:


# Display first rows
df.head()


# In[9]:


# Check data types
df.dtypes


# In[10]:


# Check data shape
df.shape


# In[11]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[12]:


get_ipython().system('uv add sqlalchemy')


# In[13]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[14]:


get_ipython().system('uv add psycopg2-binary')


# In[15]:


from sqlalchemy import create_engine
engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")


# In[16]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[17]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[18]:


df_iter = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[19]:


for df_chunk in df_iter:
    print(len(df_chunk))


# In[20]:


df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[21]:


first = True

for df_chunk in df_iter:

    if first:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))


# In[22]:


get_ipython().system('uv add tqdm')


# In[29]:


from tqdm.auto import tqdm



# In[30]:


for df_chunk in tqdm(df_iter):
   df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')







