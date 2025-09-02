@echo off
echo Setting up Indian Investment Data Collection System
echo ==================================================

echo.
echo Step 1: Creating directory structure...
mkdir yahoo_india
mkdir database
mkdir exports
mkdir logs
mkdir config

echo.
echo Step 2: Installing Python packages...
pip install -r requirements.txt

echo.
echo Step 3: Setting up MySQL database...
echo Please run the following command in MySQL:
echo mysql -u root -p ^< database/setup_database.sql

echo.
echo Step 4: Configuration...
echo Please edit config/database_config.py and add your MySQL password

echo.
echo Setup complete! 
echo.
echo Next steps:
echo 1. Set up MySQL database using database/setup_database.sql
echo 2. Update database password in config/database_config.py
echo 3. Run: python yahoo_india/dump_indian_stocks.py
echo 4. Run: python yahoo_india/dump_indian_indices.py
echo 5. Run: python exports/export_to_csv.py

pause
