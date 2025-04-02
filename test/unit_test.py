import pandas as pd
import os, sys
import pytest
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.transform import load_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_data_quality(df: pd.DataFrame):
    assert len(df['seat_type'].unique()) == 4
    assert len(df['type_of_traveller'].unique()) == 5
    assert len(df['seat_comfort'].unique()) == 6
    assert len(df['cabin_staff_service'].unique()) == 6
    assert len(df['food_and_beverages'].unique()) == 6
    assert len(df['wifi_and_connectivity'].unique()) == 6
    assert len(df['value_for_money'].unique()) == 5
    assert len(df['recommended'].unique()) == 2

    logger.info("Data quality test passed")

def main():
    df = load_data('data/cleaned_data.csv')
    test_data_quality(df)

if __name__ == '__main__':
    main()

