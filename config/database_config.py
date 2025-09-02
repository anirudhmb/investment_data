# Database configuration for Indian market data
import os

# Database connection settings
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Add your MySQL password here
    'database': 'indian_market_data',
    'charset': 'utf8mb4'
}

# Connection string for SQLAlchemy
def get_connection_string():
    config = DATABASE_CONFIG
    return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset={config['charset']}"

# Yahoo Finance settings
YAHOO_CONFIG = {
    'rate_limit_delay': 0.5,  # seconds between requests
    'max_retries': 3,
    'timeout': 30
}

# Data collection settings
DATA_CONFIG = {
    'default_start_date': '2023-01-01',
    'batch_size': 50,
    'log_level': 'INFO'
}

# Export settings
EXPORT_CONFIG = {
    'output_dir': 'exports',
    'date_format': '%Y-%m-%d',
    'decimal_places': 2
}
