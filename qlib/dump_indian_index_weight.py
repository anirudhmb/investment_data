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
import datetime
from config.database_config import get_connection_string

def dump_indian_index_weight(skip_exists=False):
    """Dump Indian index weights to Qlib format - adapted from original project"""
    sqlEngine = create_engine(get_connection_string(), pool_recycle=3600)
    dbConnection = sqlEngine.raw_connection()

    # Indian index mapping (adapted from original project)
    index_map = {
        "nifty50": "^NSEI",
        "niftybank": "^NSEBANK", 
        "niftyit": "^NSEIT",
        "niftypharma": "^NSEPHARMA",
        "niftyauto": "^NSEAUTO",
        "niftyfmcg": "^NSEFMCG",
        "niftyenergy": "^NSEENERGY",
        "niftypsu": "^NSEPSU",
        "niftyprivate": "^NSEPRIVATE",
        "sensex": "^BSESN",
        "bsebank": "^BSEBANK",
        "bseit": "^BSEIT",
        "bseauto": "^BSEAUTO",
        "bsefmcg": "^BSEFMCG",
        "bseenergy": "^BSEENERGY",
        "bsepsu": "^BSEPSU",
        "bseprivate": "^BSEPRIVATE"
    }

    script_path = os.path.dirname(os.path.realpath(__file__))
    qlib_index_dir = os.path.join(script_path, 'qlib_index')
    
    # Create qlib_index directory if it doesn't exist
    os.makedirs(qlib_index_dir, exist_ok=True)

    for index_name, index_code in index_map.items():
        filename = f'{qlib_index_dir}/{index_name}.txt'
        if skip_exists and os.path.isfile(filename):
            continue

        print("Dumping to file: ", filename)
        
        # For now, create a simple index file with major stocks
        # In a real implementation, you would get actual index weights
        major_stocks = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
            'ICICIBANK', 'KOTAKBANK', 'LT', 'SBIN', 'BHARTIARTL'
        ]
        
        # Create index weight data (simplified - equal weights for now)
        index_data = []
        for stock in major_stocks:
            index_data.append({
                'stock_code': stock,
                'start_date': '2023-01-01',
                'end_date': datetime.datetime.today().strftime('%Y-%m-%d')
            })
        
        df = pd.DataFrame(index_data)
        df.to_csv(filename, index=False, header=False, sep='\t')

if __name__ == "__main__":
    fire.Fire(dump_indian_index_weight)
