import fire
import pandas as pd
import sys
import os

# Add Qlib scripts to Python path
def setup_qlib_path():
    # Try to find Qlib repository
    possible_paths = [
        os.path.join(os.getcwd(), "qlib"),  # Current directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "qlib"),  # Relative to this script
        os.path.join(os.path.expanduser("~"), "qlib"),  # Home directory
        "/tmp/indian_qlib/qlib",  # Default working directory
    ]
    
    for path in possible_paths:
        scripts_path = os.path.join(path, "scripts")
        if os.path.exists(scripts_path):
            if scripts_path not in sys.path:
                sys.path.insert(0, scripts_path)
            print(f"✅ Found Qlib scripts at: {scripts_path}")
            return True
    
    print("❌ Qlib scripts directory not found!")
    print("Please ensure Qlib repository is cloned.")
    return False

# Setup Qlib path before importing
if not setup_qlib_path():
    print("Please run: git clone https://github.com/microsoft/qlib.git")
    sys.exit(1)

try:
    from data_collector.base import Normalize
    from data_collector.yahoo import collector as yahoo_collector
    print("✅ Successfully imported Qlib data_collector modules")
except ImportError as e:
    print("============")
    print("ATTENTION: Need to put qlib/scripts directory into PYTHONPATH")
    print("Current Python path:")
    for path in sys.path:
        print(f"  {path}")
    print("============")
    raise e

class CrowdSourceNormalize(yahoo_collector.YahooNormalizeCN1d):
    # Add vwap so that vwap will be adjusted during normalization
    COLUMNS = ["open", "close", "high", "low", "vwap", "volume"]

    def _manual_adj_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # amount should be kept as original value, so that adjusted volume * adjust vwap = amount
        result_df = super()._manual_adj_data(df)
        result_df["amount"] = df["amount"]
        return result_df

def normalize_crowd_source_data(source_dir=None, normalize_dir=None, max_workers=1, interval="1d", date_field_name="tradedate", symbol_field_name="symbol"):
    print(f"Starting normalization with Qlib data_collector...")
    print(f"Source: {source_dir}")
    print(f"Target: {normalize_dir}")
    
    yc = Normalize(
        source_dir=source_dir,
        target_dir=normalize_dir,
        normalize_class=CrowdSourceNormalize,
        max_workers=max_workers,
        date_field_name=date_field_name,
        symbol_field_name=symbol_field_name,
    )
    yc.normalize()
    print("✅ Normalization completed successfully!")

if __name__ == "__main__":
    fire.Fire(normalize_crowd_source_data)