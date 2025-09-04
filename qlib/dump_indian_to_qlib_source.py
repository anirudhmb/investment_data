import sys
import os

# Add the parent directory to Python path to find config module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import fire
from config.database_config import get_connection_string

def dump_indian_to_qlib_source(skip_exists=True):
    """Dump Indian market data to Qlib source format - adapted from original project"""
    sqlEngine = create_engine(get_connection_string(), pool_recycle=3600)
    dbConnection = sqlEngine.raw_connection()
    
    # Query Indian stock data with VWAP calculation (matching original project format)
    stock_df = pd.read_sql("""
        SELECT 
            tradedate,
            symbol,
            open,
            high,
            low,
            close,
            volume,
            adjclose,
            amount,
            amount/volume*10 as vwap
        FROM yahoo_a_stock_eod_price 
        WHERE symbol IN (
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
            'ICICIBANK', 'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL',
            'ITC', 'ASIANPAINT', 'AXISBANK', 'MARUTI', 'NESTLEIND',
            'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'WIPRO', 'POWERGRID'
        )
        ORDER BY symbol, tradedate
    """, dbConnection)
    
    dbConnection.close()
    sqlEngine.dispose()

    script_path = os.path.dirname(os.path.realpath(__file__))
    qlib_source_dir = os.path.join(script_path, 'qlib_source')
    
    # Create qlib_source directory if it doesn't exist
    os.makedirs(qlib_source_dir, exist_ok=True)

    for symbol, df in stock_df.groupby("symbol"):
        filename = f'{qlib_source_dir}/{symbol}.csv'
        print("Dumping to file: ", filename)
        if skip_exists and os.path.isfile(filename):
            continue
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    fire.Fire(dump_indian_to_qlib_source)
