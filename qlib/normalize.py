import fire
import pandas as pd
import sys
import os

# Simple Qlib path setup - relies on proper installation via batch file
def setup_qlib_path():
    """Setup Qlib path - assumes Qlib is properly installed"""
    # Check if Qlib is installed as a package (preferred method)
    try:
        import qlib
        print(f"✅ Qlib package found: {qlib.__file__}")
        return True
    except ImportError:
        pass
    
    # Fallback: Check PYTHONPATH for qlib scripts
    python_path = os.environ.get('PYTHONPATH', '')
    if python_path:
        for path in python_path.split(os.pathsep):
            if 'qlib' in path and 'scripts' in path:
                if os.path.exists(path):
                    if path not in sys.path:
                        sys.path.insert(0, path)
                    print(f"✅ Found Qlib scripts via PYTHONPATH: {path}")
                    return True
    
    print("❌ Qlib not found!")
    print("Please install Qlib using:")
    print("pip install qlib")
    return False

# Setup Qlib path before importing
if not setup_qlib_path():
    sys.exit(1)

try:
    # Import Qlib data_collector modules
    from data_collector.base import Normalize
    from data_collector.yahoo import collector as yahoo_collector
    print("✅ Successfully imported Qlib data_collector modules")
except ImportError as e:
    print("❌ Failed to import data_collector modules!")
    print(f"Error: {e}")
    print("\nPlease install Qlib using:")
    print("pip install qlib")
    raise e

class CrowdSourceNormalize(yahoo_collector.YahooNormalizeCN1d):
    # Add vwap so that vwap will be adjusted during normalization
    COLUMNS = ["open", "close", "high", "low", "vwap", "volume"]

    def _manual_adj_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # amount should be kept as original value, so that adjusted volume * adjust vwap = amount
        result_df = super()._manual_adj_data(df)
        result_df["amount"] = df["amount"]
        return result_df

def normalize_data(source_dir=None, normalize_dir=None, max_workers=1, interval="1d", date_field_name="tradedate", symbol_field_name="symbol"):
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