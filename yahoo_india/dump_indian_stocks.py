import yfinance as yf
import pandas as pd
import os
import datetime
import fire
import time
from sqlalchemy import create_engine
import pymysql

class IndianStockCollector:
    def __init__(self, db_connection_string="mysql+pymysql://root:@127.0.0.1/investment_data"):
        self.engine = create_engine(db_connection_string, pool_recycle=3600)
        
        # Indian stocks - using the same format as original project
        self.nse_stocks = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
            'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS', 'SBIN.NS', 'BHARTIARTL.NS',
            'ITC.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'MARUTI.NS', 'NESTLEIND.NS',
            'SUNPHARMA.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS', 'POWERGRID.NS'
        ]
        self.bse_stocks = [
            'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'INFY.BO', 'HINDUNILVR.BO',
            'ICICIBANK.BO', 'KOTAKBANK.BO', 'LT.BO', 'SBIN.BO', 'BHARTIARTL.BO',
            'ITC.BO', 'ASIANPAINT.BO', 'AXISBANK.BO', 'MARUTI.BO', 'NESTLEIND.BO',
            'SUNPHARMA.BO', 'TITAN.BO', 'ULTRACEMCO.BO', 'WIPRO.BO', 'POWERGRID.BO'
        ]
        
    def get_stock_data(self, symbol, start_date, end_date):
        """Fetch stock data from Yahoo Finance - adapted from original yahoo collector"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"No data found for {symbol}")
                return None
                
            # Reset index to get date as column
            data = data.reset_index()
            
            # Rename columns to match original project schema
            data = data.rename(columns={
                'Date': 'tradedate',
                'Open': 'open',
                'High': 'high', 
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # Add symbol column (convert to format compatible with original project)
            # Convert RELIANCE.NS to RELIANCE format for compatibility
            clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
            data['symbol'] = clean_symbol
            
            # Calculate adjusted close (using close for now, can be enhanced)
            data['adjclose'] = data['close']
            
            # Add amount column (volume * close for compatibility with original project)
            data['amount'] = data['volume'] * data['close']
            
            # Select required columns matching original project schema
            data = data[['tradedate', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'adjclose', 'amount']]
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_latest_date(self):
        """Get the latest date in database - adapted from original project"""
        try:
            query = """
            SELECT MAX(tradedate) as latest_date 
            FROM yahoo_a_stock_eod_price 
            WHERE tradedate > '2023-01-01'
            """
            result = pd.read_sql(query, self.engine)
            if not result.empty and result['latest_date'].iloc[0] is not None:
                return result['latest_date'].iloc[0]
            else:
                return datetime.date(2023, 1, 1)
        except:
            return datetime.date(2023, 1, 1)
    
    def update_stock_prices(self, start_date=None, end_date=None):
        """Update stock prices for all Indian stocks - adapted from original project"""
        if start_date is None:
            start_date = self.get_latest_date()
        if end_date is None:
            end_date = datetime.date.today()
            
        print(f"Updating Indian stock data from {start_date} to {end_date}")
        
        all_stocks = self.nse_stocks + self.bse_stocks
        successful_updates = 0
        
        for symbol in all_stocks:
            print(f"Processing {symbol}...")
            data = self.get_stock_data(symbol, start_date, end_date)
            
            if data is not None and not data.empty:
                try:
                    # Insert data into database using original project table name
                    data.to_sql('yahoo_a_stock_eod_price', self.engine, if_exists='append', index=False)
                    successful_updates += 1
                    print(f"✓ {symbol}: {len(data)} records updated")
                except Exception as e:
                    print(f"✗ {symbol}: Database error - {str(e)}")
            
            # Rate limiting
            time.sleep(0.5)
        
        print(f"\nUpdate complete: {successful_updates}/{len(all_stocks)} stocks updated successfully")
    
    def get_stock_list(self):
        """Get list of all stocks being tracked - adapted from original project"""
        all_stocks = self.nse_stocks + self.bse_stocks
        stock_list = []
        
        for symbol in all_stocks:
            market = 'NSE' if symbol.endswith('.NS') else 'BSE'
            stock_code = symbol.replace('.NS', '').replace('.BO', '')
            stock_list.append({
                'symbol': stock_code,  # Clean symbol for compatibility
                'ts_code': symbol,     # Original Yahoo symbol
                'name': stock_code,
                'market': market,
                'list_date': '2023-01-01',  # Default list date
                'delist_date': None
            })
        
        return pd.DataFrame(stock_list)

def main():
    collector = IndianStockCollector()
    
    # Create stock list (compatible with original project)
    stock_list = collector.get_stock_list()
    stock_list.to_sql('yahoo_stock_list', collector.engine, if_exists='replace', index=False)
    print("Indian stock list created")
    
    # Update stock prices
    collector.update_stock_prices()

if __name__ == '__main__':
    fire.Fire(main)