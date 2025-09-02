import yfinance as yf
import pandas as pd
import os
import datetime
import fire
import time
from sqlalchemy import create_engine
import pymysql

class IndianIndexCollector:
    def __init__(self, db_connection_string="mysql+pymysql://root:@127.0.0.1/investment_data"):
        self.engine = create_engine(db_connection_string, pool_recycle=3600)
        
        # Indian indices - adapted from original project structure
        self.indices = {
            '^NSEI': 'Nifty 50',
            '^NSEBANK': 'Nifty Bank', 
            '^NSEMDCP50': 'Nifty Midcap 50',
            '^NSEIT': 'Nifty IT',
            '^NSEPHARMA': 'Nifty Pharma',
            '^NSEAUTO': 'Nifty Auto',
            '^NSEFMCG': 'Nifty FMCG',
            '^NSEENERGY': 'Nifty Energy',
            '^NSEPSU': 'Nifty PSU Bank',
            '^NSEPRIVATE': 'Nifty Private Bank',
            '^BSESN': 'BSE Sensex',
            '^BSEBANK': 'BSE Bankex',
            '^BSEIT': 'BSE IT',
            '^BSEAUTO': 'BSE Auto',
            '^BSEFMCG': 'BSE FMCG',
            '^BSEENERGY': 'BSE Energy',
            '^BSEPSU': 'BSE PSU',
            '^BSEPRIVATE': 'BSE Private Bank'
        }
    
    def get_index_data(self, index_symbol, start_date, end_date):
        """Fetch index data from Yahoo Finance - adapted from original project"""
        try:
            ticker = yf.Ticker(index_symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"No data found for {index_symbol}")
                return None
                
            # Reset index to get date as column
            data = data.reset_index()
            
            # Rename columns to match original project schema
            data = data.rename(columns={
                'Date': 'trade_date',
                'Open': 'open',
                'High': 'high', 
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # Add index information (compatible with original project)
            data['index_code'] = index_symbol
            data['index_name'] = self.indices.get(index_symbol, index_symbol)
            
            # Calculate adjusted close (using close for indices)
            data['adjclose'] = data['close']
            
            # Select required columns matching original project schema
            data = data[['trade_date', 'index_code', 'index_name', 'open', 'high', 'low', 'close', 'volume', 'adjclose']]
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {index_symbol}: {str(e)}")
            return None
    
    def get_latest_index_date(self):
        """Get the latest date in index database - adapted from original project"""
        try:
            query = """
            SELECT MAX(trade_date) as latest_date 
            FROM yahoo_index_eod_price 
            WHERE trade_date > '2023-01-01'
            """
            result = pd.read_sql(query, self.engine)
            if not result.empty and result['latest_date'].iloc[0] is not None:
                return result['latest_date'].iloc[0]
            else:
                return datetime.date(2023, 1, 1)
        except:
            return datetime.date(2023, 1, 1)
    
    def update_index_prices(self, start_date=None, end_date=None):
        """Update index prices for all Indian indices - adapted from original project"""
        if start_date is None:
            start_date = self.get_latest_index_date()
        if end_date is None:
            end_date = datetime.date.today()
            
        print(f"Updating Indian index data from {start_date} to {end_date}")
        
        successful_updates = 0
        
        for index_symbol, index_name in self.indices.items():
            print(f"Processing {index_symbol} ({index_name})...")
            data = self.get_index_data(index_symbol, start_date, end_date)
            
            if data is not None and not data.empty:
                try:
                    # Insert data into database using original project table name
                    data.to_sql('yahoo_index_eod_price', self.engine, if_exists='append', index=False)
                    successful_updates += 1
                    print(f"✓ {index_symbol}: {len(data)} records updated")
                except Exception as e:
                    print(f"✗ {index_symbol}: Database error - {str(e)}")
            
            # Rate limiting
            time.sleep(0.5)
        
        print(f"\nIndex update complete: {successful_updates}/{len(self.indices)} indices updated successfully")
    
    def create_index_list(self):
        """Create index list table - adapted from original project"""
        index_list = []
        
        for index_symbol, index_name in self.indices.items():
            market = 'NSE' if 'NSE' in index_symbol or '^NSE' in index_symbol else 'BSE'
            index_list.append({
                'index_code': index_symbol,
                'index_name': index_name,
                'market': market,
                'list_date': '2023-01-01',
                'description': f"{index_name} index"
            })
        
        df = pd.DataFrame(index_list)
        df.to_sql('yahoo_index_list', self.engine, if_exists='replace', index=False)
        print("Indian index list created successfully")

def main():
    collector = IndianIndexCollector()
    
    # Create index list
    collector.create_index_list()
    
    # Update index prices
    collector.update_index_prices()

if __name__ == '__main__':
    fire.Fire(main)