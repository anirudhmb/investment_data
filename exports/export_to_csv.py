import pandas as pd
import os
import fire
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from config.database_config import get_connection_string

class IndianDataExporter:
    def __init__(self, db_connection_string=None):
        if db_connection_string is None:
            db_connection_string = get_connection_string()
        self.engine = create_engine(db_connection_string, pool_recycle=3600)
        self.output_dir = 'exports'
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def export_stock_prices(self, start_date=None, end_date=None, market=None):
        """Export stock prices to CSV"""
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        SELECT tradedate, symbol, market, open, high, low, close, volume, adjclose
        FROM indian_stock_prices 
        WHERE tradedate BETWEEN %s AND %s
        """
        params = [start_date, end_date]
        
        if market:
            query += " AND market = %s"
            params.append(market)
        
        query += " ORDER BY tradedate, symbol"
        
        df = pd.read_sql(query, self.engine, params=params)
        
        filename = f"indian_stock_prices_{start_date}_to_{end_date}"
        if market:
            filename += f"_{market}"
        filename += ".csv"
        
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Exported {len(df)} records to {filepath}")
        
        return filepath
    
    def export_index_prices(self, start_date=None, end_date=None, market=None):
        """Export index prices to CSV"""
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        SELECT tradedate, index_code, index_name, market, open, high, low, close, volume, adjclose
        FROM indian_index_prices 
        WHERE tradedate BETWEEN %s AND %s
        """
        params = [start_date, end_date]
        
        if market:
            query += " AND market = %s"
            params.append(market)
        
        query += " ORDER BY tradedate, index_code"
        
        df = pd.read_sql(query, self.engine, params=params)
        
        filename = f"indian_index_prices_{start_date}_to_{end_date}"
        if market:
            filename += f"_{market}"
        filename += ".csv"
        
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Exported {len(df)} records to {filepath}")
        
        return filepath
    
    def export_stock_list(self):
        """Export stock list to CSV"""
        query = "SELECT * FROM indian_stock_list ORDER BY market, symbol"
        df = pd.read_sql(query, self.engine)
        
        filepath = os.path.join(self.output_dir, "indian_stock_list.csv")
        df.to_csv(filepath, index=False)
        print(f"Exported {len(df)} stocks to {filepath}")
        
        return filepath
    
    def export_index_list(self):
        """Export index list to CSV"""
        query = "SELECT * FROM indian_index_list ORDER BY market, index_code"
        df = pd.read_sql(query, self.engine)
        
        filepath = os.path.join(self.output_dir, "indian_index_list.csv")
        df.to_csv(filepath, index=False)
        print(f"Exported {len(df)} indices to {filepath}")
        
        return filepath
    
    def export_all(self, start_date=None, end_date=None):
        """Export all data to CSV files"""
        print("Exporting all Indian market data...")
        
        # Export stock list
        self.export_stock_list()
        
        # Export index list
        self.export_index_list()
        
        # Export stock prices
        self.export_stock_prices(start_date, end_date)
        
        # Export index prices
        self.export_index_prices(start_date, end_date)
        
        print("All exports completed!")

def main():
    exporter = IndianDataExporter()
    fire.Fire(exporter.export_all)

if __name__ == '__main__':
    fire.Fire(IndianDataExporter)
