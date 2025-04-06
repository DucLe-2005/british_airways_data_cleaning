import pandas as pd
import config as cfg
import logging
import re
from typing import Dict, Tuple, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load the data from the csv file
def load_data(path: str) -> pd.DataFrame:
    """ 
    Load the data from the csv file
    Args:
        path (str): The path to the csv file
    Returns:
        pd.DataFrame: The dataframe
    """
    df = pd.read_csv(path)
    logger.info(f"Successfully loaded data with shape {df.shape}")
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Rename the columns of the dataframe snake case
    Args:
        df (pd.DataFrame): The dataframe to rename
    Returns:
        pd.DataFrame: The renamed dataframe
    """
    df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

    # handling edge cases of & and -
    df.columns = df.columns.str.replace("&", "and")
    df.columns = df.columns.str.replace("-", "_")
    df.rename(columns={'date': 'date_submitted', 'country': 'nationality'}, inplace=True)
    
    logger.info(f"Successfully renamed columns: {list(df.columns)}")
    return df

def clean_date_submitted_column(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Clean the date_submitted column by converting to datetime and setting the date format
    Args:
        df (pd.DataFrame): The dataframe to clean
    Returns:
        pd.DataFrame: The cleaned dataframe
    """
    # Convert date format from "19th March 2025" to "03/19/2025"
    df['date_submitted'] = df['date_submitted'].str.replace(r'(\d+)(st|nd|rd|th)', r'\1', regex=True)
    df['date_submitted'] = pd.to_datetime(df['date_submitted'], format='%d %B %Y')
    df['date_submitted'] = df['date_submitted'].dt.strftime('%Y-%m-%d')
    
    logger.info("Successfully cleaned date_submitted column")
    return df

def clean_nationality_column(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Clean the nationality column by removing the parentheses and any extra spaces
    Args:
        df (pd.DataFrame): The dataframe to clean
    Returns:
        pd.DataFrame: The cleaned dataframe
    """
    df['nationality'] = df['nationality'].str.replace(r'[()]', '', regex=True).str.strip()
    logger.info("Successfully cleaned nationality column")
    return df

def create_verify_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a verify column by checking the verification status from the review_body
    Args:
        df (pd.DataFrame): The dataframe to create the verify column
    Returns:
        pd.DataFrame: The dataframe with the verify column
    """
    verify_status = df['review_body'].str.contains('trip verified', case=False, na=False)
    
    if 'verify' in df.columns:
        df = df.drop('verify', axis=1)

    df.insert(
        loc=3, # Insert after review_body column
        column='verify',
        value=verify_status
    )
    
    logger.info(f"Successfully created verify column with {verify_status.sum()} verified reviews")
    return df

def clean_review_body(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the review_body column by removing the verification status
    Args:
        df (pd.DataFrame): The dataframe to clean
    Returns:
        pd.DataFrame: The cleaned dataframe
    """
    # Split review body on '|' and take second part, stripping whitespace
    df.loc[df['verify'], 'review_body'] = df.loc[df['verify'], 'review_body'].str.split('|').str[1].str.strip()
    
    logger.info("Successfully cleaned review_body column")
    return df

def clean_date_flown_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assume the date is the first of the month as no date is provided.
    Clean the date_flown column by converting to datetime and setting the date format YYYY-MM-DD. 
    Args:
        df (pd.DataFrame): The dataframe to clean
    Returns:
        pd.DataFrame: The cleaned dataframe
    """
    df['date_flown'] = pd.to_datetime(df['date_flown'], format='%B %Y')
    df['date_flown'] = df['date_flown'].dt.strftime('%Y-%m-%d')
    logger.info("Successfully cleaned date_flown column")
    return df

def clean_recommended_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the recommended column by converting to boolean
    Args:
        df (pd.DataFrame): The dataframe to clean
    Returns:
        pd.DataFrame: The dataframe with the recommended column converted to boolean
    """
    df['recommended'] = df['recommended'].str.contains('yes', case=False, na=False)
    logger.info(f"Successfully converted recommended column to boolean with {df['recommended'].sum()} positive recommendations")
    return df

def clean_rating_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the rating columns by converting to int, preserving NaN values
    Args:
        df (pd.DataFrame): The dataframe to clean
    Returns:
        pd.DataFrame: The cleaned dataframe
    """
    rating_columns = ['seat_comfort', 'cabin_staff_service', 'food_and_beverages', 
                     'wifi_and_connectivity', 'value_for_money']
    
    for col in rating_columns:
        # Convert to float first to preserve NaN, then to Int64 which can handle NaN
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    logger.info("Successfully cleaned all rating columns")
    return df

def parse_route(route: str) -> Dict[str, Union[str, None]]:
    """
    Parse a route string into origin, destination, and transit components,
    and further extract city and airport information.
    
    Args:
        route (str): The route string to parse (e.g., "London Heathrow to Paris CDG via Amsterdam")
        
    Returns:
        Dict: A dictionary containing the parsed components:
            - origin: The full origin string
            - destination: The full destination string
            - transit: The full transit string (if any)
            - origin_city: The extracted origin city
            - origin_airport: The extracted origin airport (3-letter IATA code)
            - destination_city: The extracted destination city
            - destination_airport: The extracted destination airport (3-letter IATA code)
            - transit_city: The extracted transit city (if any)
            - transit_airport: The extracted transit airport (3-letter IATA code)
    """
    # Map of airport codes to their cities
    AIRPORT_TO_CITY = cfg.AIRPORT_TO_CITY
    # Map of airport names/keywords to their 3-letter IATA codes
    AIRPORT_CODES = cfg.AIRPORT_CODES
    # Map of city names to their common airport codes
    CITY_TO_AIRPORT = cfg.CITY_TO_AIRPORT
    
    def extract_city_airport(location: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract city and airport from a location string.
        
        Args:
            location (str): The location string to parse (e.g., "London Heathrow", "JFK", "Paris CDG")
            
        Returns:
            Tuple[str, str]: A tuple containing (city, airport) where airport is a 3-letter IATA code
                             and city is the proper city name (not the airport code)
        """
        if not location or pd.isna(location) or location.strip() == '':
            return None, None
        
        location = location.strip().lower()
        
        # Check for 3-letter codes that might be IATA codes
        iata_match = re.search(r'\b([a-z]{3})\b', location)
        if iata_match:
            code = iata_match.group(1).upper()
            # If it's a valid code in our dictionary
            if code in AIRPORT_TO_CITY:
                # Get the city for this airport code
                city = AIRPORT_TO_CITY[code]
                return city, code
            
            # If we don't know the city for this code but it's a valid format
            if code in [v for v in AIRPORT_CODES.values()]:
                # Try to extract the city from the location
                location_without_code = re.sub(r'\b' + iata_match.group(1) + r'\b', '', location).strip()
                if location_without_code:
                    return location_without_code.title(), code
                else:
                    # If we can't determine the city, use a placeholder
                    return "Unknown", code
        
        # Check for known airport names in the location
        for airport_name, airport_code in AIRPORT_CODES.items():
            if airport_name in location:
                # Get the city for this airport code
                if airport_code in AIRPORT_TO_CITY:
                    city = AIRPORT_TO_CITY[airport_code]
                    return city, airport_code
                
                # If we don't have a mapping for this airport code
                # Extract the city part from the location
                city_part = location.replace(airport_name, '').strip()
                if city_part:
                    return city_part.title(), airport_code
                else:
                    # If we can't determine the city, use a placeholder
                    return "Unknown", airport_code
        
        # Check for city names that have default airports
        for city_name, airport_code in CITY_TO_AIRPORT.items():
            if city_name in location and len(city_name) > 3:  # Exclude 3-letter airport codes
                return city_name.title(), airport_code
        
        # If we reach here, we couldn't identify an airport code
        # Return the location as the city and None for airport
        return location.title(), None
    
    if not route or pd.isna(route) or route.strip() == '':
        return {
            'origin': None, 'destination': None, 'transit': None,
            'origin_city': None, 'origin_airport': None,
            'destination_city': None, 'destination_airport': None,
            'transit_city': None, 'transit_airport': None
        }
    
    # Normalize the route string
    route = route.strip()
    
    # Initialize result dictionary
    result = {
        'origin': None, 'destination': None, 'transit': None,
        'origin_city': None, 'origin_airport': None,
        'destination_city': None, 'destination_airport': None,
        'transit_city': None, 'transit_airport': None
    }
    
    # Check if route contains 'via' for transit
    if ' via ' in route.lower():
        parts = route.lower().split(' via ')
        main_route = parts[0]
        transit = parts[1]
        
        # Split main route into origin and destination
        if ' to ' in main_route:
            origin_dest = main_route.split(' to ')
            origin = origin_dest[0].strip()
            destination = origin_dest[1].strip() if len(origin_dest) > 1 else None
        else:
            origin = main_route.strip()
            destination = None
        
        # Store the original values
        result['origin'] = origin.title() if origin else None
        result['destination'] = destination.title() if destination else None
        result['transit'] = transit.title() if transit else None
        
        # Extract city and airport for each component
        if origin:
            origin_city, origin_airport = extract_city_airport(origin)
            result['origin_city'] = origin_city
            result['origin_airport'] = origin_airport
        
        if destination:
            dest_city, dest_airport = extract_city_airport(destination)
            result['destination_city'] = dest_city
            result['destination_airport'] = dest_airport
        
        if transit:
            transit_city, transit_airport = extract_city_airport(transit)
            result['transit_city'] = transit_city
            result['transit_airport'] = transit_airport
    
    # For routes without transit
    elif ' to ' in route.lower():
        parts = route.lower().split(' to ')
        origin = parts[0].strip()
        destination = parts[1].strip() if len(parts) > 1 else None
        
        # Store the original values
        result['origin'] = origin.title() if origin else None
        result['destination'] = destination.title() if destination else None
        
        # Extract city and airport for each component
        if origin:
            origin_city, origin_airport = extract_city_airport(origin)
            result['origin_city'] = origin_city
            result['origin_airport'] = origin_airport
        
        if destination:
            dest_city, dest_airport = extract_city_airport(destination)
            result['destination_city'] = dest_city
            result['destination_airport'] = dest_airport
    
    # For single location (unlikely but handling edge case)
    else:
        origin = route.strip()
        result['origin'] = origin.title()
        
        # Extract city and airport
        origin_city, origin_airport = extract_city_airport(origin)
        result['origin_city'] = origin_city
        result['origin_airport'] = origin_airport
    
    return result

def cleaning_route_column(df: pd.DataFrame, route_column: str = 'route') -> pd.DataFrame:
    """
    Process a DataFrame containing route information.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the route information
        route_column (str): The name of the column containing the route strings
        
    Returns:
        pd.DataFrame: The processed DataFrame with added columns for route components
    """
    if route_column not in df.columns:
        raise ValueError(f"Column '{route_column}' not found in DataFrame")
    
    # Apply the parse_route function to each route
    route_components = df[route_column].apply(parse_route)
    
    # Extract the components into separate columns
    df['origin'] = route_components.apply(lambda x: x['origin'])
    df['destination'] = route_components.apply(lambda x: x['destination'])
    df['transit'] = route_components.apply(lambda x: x['transit'])
    df['origin_city'] = route_components.apply(lambda x: x['origin_city'])
    df['origin_airport'] = route_components.apply(lambda x: x['origin_airport'])
    df['destination_city'] = route_components.apply(lambda x: x['destination_city'])
    df['destination_airport'] = route_components.apply(lambda x: x['destination_airport'])
    df['transit_city'] = route_components.apply(lambda x: x['transit_city'])
    df['transit_airport'] = route_components.apply(lambda x: x['transit_airport'])
    
    df.drop(['origin', 'transit', 'destination', 'route'], axis=1, inplace=True)

    logger.info("Successfully cleaned all routes columns")
    return df


def main():
    df = load_data('data/raw_data.csv')

    df = rename_columns(df)
    df = clean_date_submitted_column(df)
    df = clean_nationality_column(df)
    df = create_verify_column(df)
    df = clean_review_body(df)
    df = clean_date_flown_column(df)
    df = clean_recommended_column(df)
    df = clean_rating_columns(df)
    df = cleaning_route_column(df)

    df.to_csv('data/cleaned_data.csv', index=False)
    logger.info("Data cleaning process completed successfully")

if __name__ == '__main__':
    main()
