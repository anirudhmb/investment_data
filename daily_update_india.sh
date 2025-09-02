#!/bin/bash
# Daily update script for Indian market data - adapted from original project
set -e
set -x

echo "Starting daily update for Indian market data..."

# Update Indian stock prices
echo "Updating Indian stock prices..."
python3 yahoo_india/dump_indian_stocks.py

# Update Indian index prices  
echo "Updating Indian index prices..."
python3 yahoo_india/dump_indian_indices.py

# Run validation
echo "Running data validation..."
mysql -u root -p investment_data < yahoo_india/validation_india.sql

echo "Daily update completed successfully!"
