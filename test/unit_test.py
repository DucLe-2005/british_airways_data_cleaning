import pandas as pd
import os, sys
import pytest
import logging
from typing import Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
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

def validate_route_columns(df: pd.DataFrame) -> Dict:
    """
    Validate the processed route data.
    
    Args:
        df (pd.DataFrame): The processed DataFrame
        
    Returns:
        Dict: A dictionary containing validation results
    """
    # Count missing values
    missing_values = df[['origin_city', 'origin_airport', 'destination_city', 
                         'destination_airport', 'transit_city', 'transit_airport']].isna().sum()
    
    # Count rows with at least origin and destination
    valid_routes = df[['origin_city', 'destination_city']].notna().all(axis=1).sum()
    
    # Count routes with transit
    routes_with_transit = df['transit_city'].notna().sum()
    
    # Count routes with airport information
    routes_with_origin_airport = df['origin_airport'].notna().sum()
    routes_with_destination_airport = df['destination_airport'].notna().sum()
    routes_with_transit_airport = df['transit_airport'].notna().sum()
    
    # Validate that all airport codes are 3-letter IATA codes
    valid_airport_codes = 0
    for idx, row in df.iterrows():
        valid_origin = pd.isna(row['origin_airport']) or (isinstance(row['origin_airport'], str) and len(row['origin_airport']) == 3 and row['origin_airport'].isupper())
        valid_dest = pd.isna(row['destination_airport']) or (isinstance(row['destination_airport'], str) and len(row['destination_airport']) == 3 and row['destination_airport'].isupper())
        valid_transit = pd.isna(row['transit_airport']) or (isinstance(row['transit_airport'], str) and len(row['transit_airport']) == 3 and row['transit_airport'].isupper())
        
        if valid_origin and valid_dest and valid_transit:
            valid_airport_codes += 1
    
    # Validate that cities are not airport codes
    valid_city_names = 0
    for idx, row in df.iterrows():
        valid_origin_city = pd.isna(row['origin_city']) or (isinstance(row['origin_city'], str) and (len(row['origin_city']) != 3 or not row['origin_city'].isupper()))
        valid_dest_city = pd.isna(row['destination_city']) or (isinstance(row['destination_city'], str) and (len(row['destination_city']) != 3 or not row['destination_city'].isupper()))
        valid_transit_city = pd.isna(row['transit_city']) or (isinstance(row['transit_city'], str) and (len(row['transit_city']) != 3 or not row['transit_city'].isupper()))
        
        if valid_origin_city and valid_dest_city and valid_transit_city:
            valid_city_names += 1
    
    validation_results = {
        'total_rows': len(df),
        'valid_routes': valid_routes,
        'routes_with_transit': routes_with_transit,
        'routes_with_origin_airport': routes_with_origin_airport,
        'routes_with_destination_airport': routes_with_destination_airport,
        'routes_with_transit_airport': routes_with_transit_airport,
        'valid_airport_codes': valid_airport_codes,
        'valid_city_names': valid_city_names,
        'missing_values': missing_values.to_dict()
    }
    
    return validation_results

def main():
    df = load_data('data/cleaned_data.csv')
    validate_route_results = validate_route_columns(df)
    test_data_quality(df)
    print(validate_route_results)

if __name__ == '__main__':
    main()

