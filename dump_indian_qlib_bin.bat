@echo off
REM Dump Indian market data to Qlib binary format - Windows version
setlocal enabledelayedexpansion

REM Set working directory (default to temp folder)
set WORKING_DIR=%1
if "%WORKING_DIR%"=="" set WORKING_DIR=%TEMP%\indian_qlib

REM Set Qlib repository
set QLIB_REPO=%2
if "%QLIB_REPO%"=="" set QLIB_REPO=https://github.com/microsoft/qlib.git

echo Creating working directory...
if not exist "%WORKING_DIR%" mkdir "%WORKING_DIR%"

REM Clone Qlib if not exists
if not exist "%WORKING_DIR%\qlib" (
    echo Cloning Qlib repository...
    git clone "%QLIB_REPO%" "%WORKING_DIR%\qlib"
)

REM Create qlib source directory
if not exist "qlib\qlib_source" mkdir "qlib\qlib_source"
if not exist "qlib\qlib_index" mkdir "qlib\qlib_index"

REM Dump Indian stock data to Qlib source format
echo Dumping Indian stock data to Qlib source format...
python qlib\dump_indian_to_qlib_source.py

REM Dump Indian index weights
echo Dumping Indian index weights...
python qlib\dump_indian_index_weight.py

REM Set up Python path for Qlib
set PYTHONPATH=%PYTHONPATH%;%WORKING_DIR%\qlib\scripts

REM Normalize data using Qlib
echo Normalizing Indian market data...
python qlib\normalize.py normalize_data --source_dir qlib\qlib_source\ --normalize_dir qlib\qlib_normalize --max_workers=4 --date_field_name=tradedate --symbol_field_name=symbol

REM Convert to Qlib binary format
echo Converting to Qlib binary format...
python "%WORKING_DIR%\qlib\scripts\dump_bin.py" dump_all --data_path qlib\qlib_normalize\ --qlib_dir "%WORKING_DIR%\indian_qlib_bin" --date_field_name=tradedate --exclude_fields=tradedate,symbol

REM Copy index files to Qlib binary directory
echo Copying index files...
if not exist "%WORKING_DIR%\indian_qlib_bin\instruments" mkdir "%WORKING_DIR%\indian_qlib_bin\instruments"
if exist "qlib\qlib_index\*.txt" (
    copy "qlib\qlib_index\*.txt" "%WORKING_DIR%\indian_qlib_bin\instruments\"
) else (
    echo No index files to copy
)

REM Create trading calendar
echo Creating Indian trading calendar...
python -c "
import pandas as pd
import datetime
import os

# Create a simple trading calendar for Indian markets
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date.today()

# Generate all dates
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Filter out weekends (Saturday=5, Sunday=6)
trading_dates = all_dates[all_dates.weekday < 5]

# Create calendar file
calendar_data = pd.DataFrame({
    'date': trading_dates,
    'is_trading_day': True
})

# Add some major Indian holidays (simplified)
holidays = [
    '2024-01-26',  # Republic Day
    '2024-03-08',  # Holi
    '2024-03-29',  # Good Friday
    '2024-04-11',  # Eid
    '2024-04-17',  # Ram Navami
    '2024-05-01',  # Labour Day
    '2024-08-15',  # Independence Day
    '2024-08-26',  # Janmashtami
    '2024-10-02',  # Gandhi Jayanti
    '2024-10-12',  # Dussehra
    '2024-11-01',  # Diwali
    '2024-11-15',  # Guru Nanak Jayanti
]

for holiday in holidays:
    holiday_date = pd.to_datetime(holiday)
    if holiday_date in calendar_data['date'].values:
        calendar_data.loc[calendar_data['date'] == holiday_date, 'is_trading_day'] = False

# Save calendar
calendar_file = os.path.join(r'%WORKING_DIR%\indian_qlib_bin', 'calendars', 'indian_calendar.txt')
os.makedirs(os.path.dirname(calendar_file), exist_ok=True)
calendar_data.to_csv(calendar_file, index=False, header=False, sep='\t')
print(f'Indian trading calendar created: {calendar_file}')
"

REM Create tarball (using PowerShell since tar might not be available)
echo Creating tarball...
powershell -Command "Compress-Archive -Path '%WORKING_DIR%\indian_qlib_bin' -DestinationPath 'indian_qlib_bin.zip' -Force"

echo Indian Qlib binary data created successfully!
echo Tarball location: %CD%\indian_qlib_bin.zip

REM Copy to output directory if specified
set OUTPUT_DIR=%OUTPUT_DIR%
if not "%OUTPUT_DIR%"=="" (
    if exist "%OUTPUT_DIR%" (
        copy "indian_qlib_bin.zip" "%OUTPUT_DIR%\"
        echo Tarball copied to: %OUTPUT_DIR%\indian_qlib_bin.zip
    )
)

echo.
echo Process completed successfully!
pause
