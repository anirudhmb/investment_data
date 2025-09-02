# 🇮🇳 Indian Market Data Collection - Adapted from Original Project

This is an **adapted version** of the original investment_data project, specifically configured for Indian markets (NSE/BSE) while maintaining compatibility with the original project's architecture and capabilities.

## 🎯 **Why This Approach?**

Instead of creating a completely new system, this adaptation:
- ✅ **Leverages existing Qlib conversion capabilities**
- ✅ **Uses proven data validation and merging logic**
- ✅ **Maintains compatibility with original project structure**
- ✅ **Provides all the advanced features** (normalization, binary format, etc.)
- ✅ **Works with local MySQL database** (no Dolt required for initial testing)

## 🚀 **Quick Start**

### **Step 1: Setup Environment**
```bash
# Install Python dependencies (same as original project)
pip install -r requirements.txt

# Install MySQL and create database
mysql -u root -p < database/setup_indian_database.sql
```

### **Step 2: Collect Indian Market Data**
```bash
# Collect stock data for major Indian stocks
python3 yahoo_india/dump_indian_stocks.py

# Collect index data (Nifty, Sensex, etc.)
python3 yahoo_india/dump_indian_indices.py
```

### **Step 3: Convert to Qlib Format**
```bash
# Convert to Qlib binary format (same as original project)
bash dump_indian_qlib_bin.sh
```

### **Step 4: Daily Updates**
```bash
# Run daily updates
bash daily_update_india.sh
```

## 📊 **Data Coverage**

### **Stocks (20 major stocks each from NSE & BSE)**
- **NSE**: RELIANCE, TCS, HDFCBANK, INFY, HINDUNILVR, ICICIBANK, KOTAKBANK, LT, SBIN, BHARTIARTL, ITC, ASIANPAINT, AXISBANK, MARUTI, NESTLEIND, SUNPHARMA, TITAN, ULTRACEMCO, WIPRO, POWERGRID
- **BSE**: Same stocks with .BO suffix

### **Indices (18 major indices)**
- **NSE**: Nifty 50, Nifty Bank, Nifty Midcap 50, Nifty IT, Nifty Pharma, Nifty Auto, Nifty FMCG, Nifty Energy, Nifty PSU Bank, Nifty Private Bank
- **BSE**: Sensex, Bankex, IT, Auto, FMCG, Energy, PSU, Private Bank

## 🏗️ **Architecture (Same as Original Project)**

```
Yahoo Finance → Data Collection → MySQL Database → Validation → Qlib Format → Binary Export
```

### **Key Components**

1. **Data Collection** (`yahoo_india/`)
   - `dump_indian_stocks.py`: Stock data collection
   - `dump_indian_indices.py`: Index data collection
   - `validation_india.sql`: Data validation queries

2. **Qlib Conversion** (`qlib/`)
   - `dump_indian_to_qlib_source.py`: Convert to Qlib source format
   - `dump_indian_index_weight.py`: Index weight processing
   - `normalize.py`: Data normalization (reused from original)

3. **Database** (`database/`)
   - `setup_indian_database.sql`: Database schema (compatible with original)

4. **Automation**
   - `daily_update_india.sh`: Daily update pipeline
   - `dump_indian_qlib_bin.sh`: Qlib binary export

## 🔄 **Data Flow (Same as Original Project)**

1. **Collection**: Yahoo Finance API → MySQL database
2. **Validation**: SQL validation queries ensure data quality
3. **Processing**: Convert to Qlib source format
4. **Normalization**: Apply Qlib normalization (same as original)
5. **Binary Export**: Create Qlib binary format for ML research

## 📁 **File Structure**

```
investment_data/
├── yahoo_india/                    # Indian market data collection
│   ├── dump_indian_stocks.py      # Stock data collection
│   ├── dump_indian_indices.py     # Index data collection
│   └── validation_india.sql       # Data validation
├── qlib/                          # Qlib conversion (adapted)
│   ├── dump_indian_to_qlib_source.py
│   ├── dump_indian_index_weight.py
│   └── normalize.py               # Reused from original
├── database/                      # Database setup
│   └── setup_indian_database.sql
├── daily_update_india.sh          # Daily update script
├── dump_indian_qlib_bin.sh        # Qlib binary export
└── requirements.txt               # Same as original project
```

## 🎯 **Key Advantages Over Standalone System**

### **1. Qlib Integration**
- ✅ **Automatic normalization** using proven Qlib algorithms
- ✅ **Binary format export** for efficient ML training
- ✅ **Index weight management** for portfolio construction
- ✅ **Trading calendar integration** for backtesting

### **2. Data Quality**
- ✅ **Validation queries** ensure data integrity
- ✅ **Error handling** and logging
- ✅ **Incremental updates** (only new data)
- ✅ **Rate limiting** to respect API limits

### **3. Scalability**
- ✅ **Easy to add more stocks/indices**
- ✅ **Compatible with original project's data sources**
- ✅ **Can integrate with Dolt for version control later**
- ✅ **Supports multiple data sources** (can add Tushare, etc.)

## 🛠️ **Customization**

### **Adding More Stocks**
Edit `yahoo_india/dump_indian_stocks.py`:
```python
self.nse_stocks = [
    'RELIANCE.NS', 'TCS.NS', 
    'YOUR_STOCK.NS'  # Add your stock here
]
```

### **Adding More Indices**
Edit `yahoo_india/dump_indian_indices.py`:
```python
self.indices = {
    '^NSEI': 'Nifty 50',
    'YOUR_INDEX': 'Your Index Name'  # Add your index here
}
```

## 📈 **Usage Examples**

### **Get Stock Data**
```python
from yahoo_india.dump_indian_stocks import IndianStockCollector

collector = IndianStockCollector()
collector.update_stock_prices('2024-01-01', '2024-01-31')
```

### **Convert to Qlib Format**
```bash
# This creates the same Qlib binary format as the original project
bash dump_indian_qlib_bin.sh
```

### **Use with Qlib**
```python
import qlib
from qlib.data import D

# Initialize Qlib with Indian data
qlib.init(provider_uri="path/to/indian_qlib_bin")

# Get data (same API as original project)
data = D.features(["RELIANCE", "TCS"], ["$close", "$volume"])
```

## 🔧 **Database Schema (Compatible with Original)**

The database uses the same table structure as the original project:
- `yahoo_a_stock_eod_price`: Stock price data
- `yahoo_index_eod_price`: Index price data
- `final_a_stock_eod_price`: Final merged data
- `yahoo_india_link_table`: Data validation and linking

## 🚀 **Next Steps**

1. **Test with small dataset** first
2. **Verify Qlib integration** works correctly
3. **Add more stocks/indices** as needed
4. **Set up daily automation** using cron/Windows Task Scheduler
5. **Consider Dolt integration** for version control later

## 💡 **Pro Tips**

- **Start small**: Test with a few stocks first
- **Check logs**: Monitor `logs/` directory for any issues
- **Validate data**: Run validation queries regularly
- **Backup database**: Regular backups of your MySQL database
- **Monitor API limits**: Yahoo Finance has rate limits

## 🤝 **Contributing**

This adaptation maintains compatibility with the original project, so you can:
- **Contribute back** to the original project
- **Add new data sources** (Tushare, Alpha Vantage, etc.)
- **Improve validation** logic
- **Enhance Qlib integration**

## 📝 **Notes**

- **No Dolt required**: Uses local MySQL for initial testing
- **Same Qlib format**: Compatible with all Qlib tools and examples
- **Proven architecture**: Based on battle-tested original project
- **Easy migration**: Can later integrate with Dolt if needed

This approach gives you all the benefits of the original project while being specifically tailored for Indian markets! 🎉
