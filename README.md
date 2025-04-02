# ✈️ British Airways Data Cleaning Project

This project focuses on cleaning and preprocessing customer review data from British Airways. The data includes customer feedback, ratings, and various aspects of their flight experience.

## 🔍 Data Cleaning Steps

### 1️⃣ Column Renaming (`rename_columns`)

- Convert column names to snake case
- Handle special characters (&, -)
- Rename 'date' to 'date_submitted'
- Process:
  - Convert to lowercase
  - Replace spaces with underscores
  - Remove special characters
  - Handle multiple underscores

### 2️⃣ Date Formatting (`clean_date_submitted_column`)

- Clean date_submitted column
- Process:
  - Remove ordinal indicators (st, nd, rd, th) using regex
  - Convert to datetime using format '%d %B %Y'
  - Format output as 'MM/DD/YYYY'
- Example: "19th March 2025" → "03/19/2025"

### 3️⃣ Country Column Cleaning (`clean_country_column`)

- Clean country names
- Process:
  - Remove parentheses and their contents
  - Strip leading/trailing whitespace
  - Handle empty strings
- Example: "United Kingdom (UK)" → "United Kingdom"

### 4️⃣ Review Verification (`create_verify_column`)

- Create verify column
- Process:
  - Extract verification status from review_body
  - Create boolean column 'verify'
  - Set True for verified reviews
  - Set False for unverified reviews

### 5️⃣ Review Body Cleaning (`clean_review_body`)

- Clean review content
- Process:
  - Remove verification status text
  - Remove "trip verified" text
  - Preserve original review content
- Example: "Trip Verified | Great flight..." → "Great flight..."

### 6️⃣ Date Flown Column (`clean_date_flown_column`)

- Clean flight dates
- Process:
  - Convert to datetime
  - Set all dates to first of month
  - Format as 'MM/DD/YYYY'
- Example: "March 2025" → "03/01/2025"

### 7️⃣ Rating Columns (`clean_rating_columns`)

- Clean rating columns (seat_comfort, cabin_staff_service, etc.)
- Process:
  - Convert ratings to integers while preserving NaN values
  - Use Int64 dtype to handle missing values
  - Applies to columns:
    - seat_comfort
    - cabin_staff_service
    - food_and_beverages
    - wifi_and_connectivity
    - value_for_money

## 📚 Dependencies

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=flat&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/seaborn-%23123.svg?style=flat&logo=seaborn&logoColor=white)

## 🚀 Usage

1. Clone the repository
2. Install dependencies
3. Run the Jupyter notebook in `notebooks/data_cleaning.ipynb`

## 📊 Data Format

The cleaned dataset includes the following columns:

| Column Name         | Description                                                   | Expected Values                                     |
| ------------------- | ------------------------------------------------------------- | --------------------------------------------------- |
| `date_submitted`    | Review submission date                                        | "MM/DD/YYYY" (e.g., "03/19/2025")                   |
| `customer_name`     | Name of the reviewer                                          | String (e.g., "John Smith")                         |
| `country`           | Reviewer's country                                            | String without parentheses (e.g., "United Kingdom") |
| `verify`            | Verification status                                           | Boolean (True/False)                                |
| `review_body`       | Review content                                                | String without verification text                    |
| `aircraft`          | Aircraft type                                                 | String (e.g., "Boeing 777-300")                     |
| `type_of_traveller` | Traveler category                                             | String (e.g., "Business", "Leisure")                |
| `seat_type`         | Class of service                                              | String (e.g., "Business Class", "Economy")          |
| `route`             | Flight route                                                  | String (e.g., "London to New York")                 |
| `date_flown`        | Flight date                                                   | "MM/DD/YYYY" (e.g., "03/01/2025")                   |
| Rating columns      | Various ratings (`seat_comfort`, `cabin_staff_service`, etc.) | Integer (1-5) or Float (1.0-5.0)                    |
| `value_for_money`   | Rating for value                                              | Integer (1-5) or Float (1.0-5.0)                    |
| `recommended`       | Whether the flight was recommended                            | Boolean (True/False)                                |
