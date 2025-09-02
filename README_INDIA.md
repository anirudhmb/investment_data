# 🇮🇳 Indian Market Data Collection System

A complete system for collecting, storing, and exporting Indian stock market data (NSE/BSE) using Yahoo Finance.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Run the setup script
setup_windows.bat

# Or manually:
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Install MySQL and create database
mysql -u root -p < database/setup_database.sql
```

### 3. Configuration
Edit `config/database_config.py` and add your MySQL password:
```python
DATABASE_CONFIG = {
    'password': 'your_mysql_password_here'
}
```

### 4. Collect Data
```bash
# Collect stock data
python yahoo_india/dump_indian_stocks.py

# Collect index data
python yahoo_india/dump_indian_indices.py
```

### 5. Export Data
```bash
# Export all data to CSV
python exports/export_to_csv.py

# Export specific data
python exports/export_to_csv.py export_stock_prices --start_date=2024-01-01 --end_date=2024-01-31
```

## 📊 Data Coverage

### Stocks (NSE & BSE)
- **NSE**: RELIANCE, TCS, HDFCBANK, INFY, HINDUNILVR, ICICIBANK, KOTAKBANK, LT, SBIN, BHARTIARTL, ITC, ASIANPAINT, AXISBANK, MARUTI, NESTLEIND, SUNPHARMA, TITAN, ULTRACEMCO, WIPRO, POWERGRID
- **BSE**: Same stocks with .BO suffix

### Indices
- **NSE**: Nifty 50, Nifty Bank, Nifty Midcap 50, Nifty IT, Nifty Pharma, Nifty Auto, Nifty FMCG, Nifty Energy, Nifty PSU Bank, Nifty Private Bank
- **BSE**: Sensex, Bankex, IT, Auto, FMCG, Energy, PSU, Private Bank

## 🗄️ Database Schema

### Tables
- `indian_stock_prices`: Daily stock price data
- `indian_stock_list`: List of tracked stocks
- `indian_index_prices`: Daily index price data
- `indian_index_list`: List of tracked indices
- `indian_trading_calendar`: Trading days and holidays

## 🔄 Daily Updates

```bash
# Run daily update
python daily_update_india.py
```

## 📁 File Structure
```
indian_investment_data/
├── yahoo_india/
│   ├── dump_indian_stocks.py      # Stock data collection
│   └── dump_indian_indices.py     # Index data collection
├── database/
│   └── setup_database.sql         # Database schema
├── exports/
│   └── export_to_csv.py           # Data export utilities
├── config/
│   └── database_config.py         # Configuration
├── logs/                          # Log files
├── daily_update_india.py          # Daily update script
├── setup_windows.bat              # Windows setup script
└── requirements.txt               # Python dependencies
```

## 🛠️ Customization

### Adding More Stocks
Edit `yahoo_india/dump_indian_stocks.py`:
```python
self.nse_stocks = [
    'RELIANCE.NS', 'TCS.NS', 
    'YOUR_STOCK.NS'  # Add your stock here
]
```

### Adding More Indices
Edit `yahoo_india/dump_indian_indices.py`:
```python
self.indices = {
    '^NSEI': 'Nifty 50',
    'YOUR_INDEX': 'Your Index Name'  # Add your index here
}
```

## 📈 Usage Examples

### Get Stock Data
```python
from yahoo_india.dump_indian_stocks import IndianStockCollector

collector = IndianStockCollector()
collector.update_stock_prices('2024-01-01', '2024-01-31')
```

### Export Data
```python
from exports.export_to_csv import IndianDataExporter

exporter = IndianDataExporter()
exporter.export_stock_prices('2024-01-01', '2024-01-31', 'NSE')
```

## 🔧 Troubleshooting

### Common Issues
1. **MySQL Connection Error**: Check password in `config/database_config.py`
2. **No Data Retrieved**: Check internet connection and Yahoo Finance availability
3. **Rate Limiting**: Script includes delays, but you can adjust in config

### Logs
Check `logs/daily_update.log` for detailed execution logs.

## 📝 Notes
- Data is collected from Yahoo Finance (free)
- Includes rate limiting to respect API limits
- Supports both NSE and BSE markets
- Automatic handling of trading holidays
- CSV export for easy analysis

## 🤝 Contributing
Feel free to add more stocks, indices, or improve the data collection logic!
