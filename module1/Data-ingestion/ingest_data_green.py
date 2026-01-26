#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

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


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""
    # prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green'
    # url = f'{prefix}/green_tripdata_{year}-{month:02d}.csv.gz'

    url_green11_2025 = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Read parquet file using pandas (supports URLs directly)
    # Note: pandas read_parquet doesn't support iterator/chunksize like read_csv,
    # so we read the entire file and then chunk it manually
    # Parquet files are already compressed and efficient, so this is usually fine
    print("Reading parquet file from URL...")
    df = pd.read_parquet(url_green11_2025)
    
    print(f"File loaded: {len(df)} rows. Processing in chunks of {chunksize}...")
    first = True
    
    # Process the dataframe in chunks
    total_chunks = (len(df) // chunksize) + (1 if len(df) % chunksize > 0 else 0)
    
    for i in tqdm(range(0, len(df), chunksize), desc="Processing chunks", total=total_chunks):
        df_chunk = df.iloc[i:i+chunksize]
        
        if first:
            # Create table schema using first chunk
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False
        
        # Insert chunk into database
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )

if __name__ == '__main__':
    run()