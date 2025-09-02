#!/usr/bin/env python3
"""
Daily update script for Indian market data
This script updates stock prices and index data from Yahoo Finance
"""

import os
import sys
import datetime
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from yahoo_india.dump_indian_stocks import IndianStockCollector
from yahoo_india.dump_indian_indices import IndianIndexCollector
from config.database_config import get_connection_string

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_update.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Main function to run daily updates"""
    try:
        logging.info("Starting daily update for Indian market data")
        
        # Get connection string
        connection_string = get_connection_string()
        
        # Update stock prices
        logging.info("Updating stock prices...")
        stock_collector = IndianStockCollector(connection_string)
        stock_collector.update_stock_prices()
        
        # Update index prices
        logging.info("Updating index prices...")
        index_collector = IndianIndexCollector(connection_string)
        index_collector.update_index_prices()
        
        logging.info("Daily update completed successfully")
        
    except Exception as e:
        logging.error(f"Error during daily update: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
