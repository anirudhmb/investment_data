#!/bin/bash
# Dump Indian market data to Qlib binary format - adapted from original project
set -e
set -x

WORKING_DIR=${1:-/tmp/indian_qlib} 
QLIB_REPO=${2:-https://github.com/microsoft/qlib.git} 

# Create working directory
mkdir -p $WORKING_DIR

# Clone Qlib if not exists
[ ! -d "$WORKING_DIR/qlib" ] && git clone $QLIB_REPO "$WORKING_DIR/qlib"

# Start MySQL server (assuming it's running locally)
# You may need to adjust this based on your MySQL setup

# Create qlib source directory
mkdir -p ./qlib/qlib_source
mkdir -p ./qlib/qlib_index

# Dump Indian stock data to Qlib source format
echo "Dumping Indian stock data to Qlib source format..."
python3 ./qlib/dump_indian_to_qlib_source.py

# Dump Indian index weights
echo "Dumping Indian index weights..."
python3 ./qlib/dump_indian_index_weight.py

# Set up Python path for Qlib
export PYTHONPATH=$PYTHONPATH:$WORKING_DIR/qlib/scripts

# Normalize data using Qlib (adapted from original project)
echo "Normalizing Indian market data..."
python3 ./qlib/normalize.py normalize_data \
    --source_dir ./qlib/qlib_source/ \
    --normalize_dir ./qlib/qlib_normalize \
    --max_workers=4 \
    --date_field_name="tradedate" \
    --symbol_field_name="symbol"

# Convert to Qlib binary format
echo "Converting to Qlib binary format..."
python3 $WORKING_DIR/qlib/scripts/dump_bin.py dump_all \
    --data_path ./qlib/qlib_normalize/ \
    --qlib_dir $WORKING_DIR/indian_qlib_bin \
    --date_field_name=tradedate \
    --exclude_fields=tradedate,symbol

# Copy index files to Qlib binary directory
echo "Copying index files..."
mkdir -p $WORKING_DIR/indian_qlib_bin/instruments/
cp qlib/qlib_index/*.txt $WORKING_DIR/indian_qlib_bin/instruments/ 2>/dev/null || echo "No index files to copy"

# Create trading calendar (simplified for Indian markets)
echo "Creating Indian trading calendar..."
python3 -c "
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
calendar_file = os.path.join('$WORKING_DIR/indian_qlib_bin', 'calendars', 'indian_calendar.txt')
os.makedirs(os.path.dirname(calendar_file), exist_ok=True)
calendar_data.to_csv(calendar_file, index=False, header=False, sep='\t')
print(f'Indian trading calendar created: {calendar_file}')
"

# Create tarball
echo "Creating tarball..."
tar -czvf ./indian_qlib_bin.tar.gz $WORKING_DIR/indian_qlib_bin/

echo "Indian Qlib binary data created successfully!"
echo "Tarball location: $(pwd)/indian_qlib_bin.tar.gz"
ls -lh ./indian_qlib_bin.tar.gz

# Copy to output directory if specified
OUTPUT_DIR=${OUTPUT_DIR:-/output}
if [ -d "${OUTPUT_DIR}" ]; then
    cp ./indian_qlib_bin.tar.gz "${OUTPUT_DIR}/"
    echo "Tarball copied to: ${OUTPUT_DIR}/indian_qlib_bin.tar.gz"
fi
