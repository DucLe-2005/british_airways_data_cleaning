import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys
import logging

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

    df.to_csv('data/cleaned_data.csv', index=False)
    logger.info("Data cleaning process completed successfully")

if __name__ == '__main__':
    main()
