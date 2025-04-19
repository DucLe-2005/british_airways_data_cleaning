# ✈️ British Airways Data Cleaning

This project focuses on cleaning and preprocessing customer review data from British Airways. The data includes customer feedback, ratings, and various aspects of their flight experience.


## ⚙️ Technology Stack
![BritishAirways (1)](https://github.com/user-attachments/assets/b903da11-27ae-412d-ad2e-3067e8f7aa04)

- **Data Source**: [British Airways Reviews on AirlineQuality](https://www.airlinequality.com/airline-reviews/british-airways/)
- **Programming Language**: Python 3.12.5  

## 🔍 Data Cleaning Steps

### 1️⃣ Load Data (`load_data`)
- Load the data from the CSV file
- Process:
  - Read CSV file using pandas
  - Log the shape of the loaded data

### 2️⃣ Column Renaming (`rename_columns`)

- Convert column names to snake case
- Handle special characters (&, -)
- Rename 'date' to 'date_submitted'
- Rename 'country' to 'nationality'
- Process:
  - Convert to lowercase
  - Replace spaces with underscores
  - Replace "&" with "and"
  - Replace "-" with "_"

### 3️⃣ Date Formatting (`clean_date_submitted_column`)

- Clean date_submitted column
- Process:
  - Remove ordinal indicators (st, nd, rd, th) using regex
  - Convert to datetime using format '%d %B %Y'
  - Format output as 'YYYY-MM-DD'
- Example: "19th March 2025" → "2025-03-19"

### 4️⃣ Nationality Column Cleaning (`clean_nationality_column`)

- Clean nationality names
- Process:
  - Remove parentheses and their contents
  - Strip leading/trailing whitespace
- Example: "United Kingdom (UK)" → "United Kingdom"

### 5️⃣ Review Verification (`create_verify_column`)

- Create verify column
- Process:
  - Extract verification status from review_body
  - Create boolean column 'verify'
  - Set True for verified reviews
  - Set False for unverified reviews
  - Insert column after review_body

### 6️⃣ Review Body Cleaning (`clean_review_body`)

- Clean review content
- Process:
  - For verified reviews, split on '|' and take second part
  - Strip whitespace
- Example: "Trip Verified | Great flight..." → "Great flight..."

### 7️⃣ Date Flown Column (`clean_date_flown_column`)

- Clean flight dates
- Process:
  - Convert to datetime using format '%B %Y'
  - Format as 'YYYY-MM-DD'
- Example: "March 2025" → "2025-03-01"

### 8️⃣ Recommended Column Cleaning (`clean_recommended_column`)

- Clean recommended column
- Process:
  - Convert to boolean
  - Set True for "yes" values
  - Set False for other values

### 9️⃣ Rating Columns (`clean_rating_columns`)

- Clean rating columns (seat_comfort, cabin_staff_service, etc.)
- Process:
  - Convert ratings to numeric using pd.to_numeric
  - Convert to Int64 dtype to handle missing values
  - Applies to columns:
    - seat_comfort
    - cabin_staff_service
    - food_and_beverages
    - wifi_and_connectivity
    - value_for_money

### 🔟 Route Column Processing (`clean_route_column`)

- Process route information into detailed components
- Extract and create new columns:
  - origin_city
  - origin_airport
  - destination_city
  - destination_airport
  - transit_city
  - transit_airport
- Process:
  - Parse route strings using airport and city mappings
  - Handle direct and connecting flights
  - Extract IATA codes and city names
  - Remove original route column

### 1️⃣1️⃣ Aircraft Column Cleaning (`clean_aircraft_column`)

- Clean and standardize aircraft information
- Process:
  - Remove unnecessary text like "Aircraft:" prefix
  - Standardize common aircraft names
  - Handle variations in Boeing and Airbus nomenclature
  - Strip whitespace and normalize formatting
- Example: "Aircraft: B777-300" → "Boeing 777-300"

### 1️⃣2️⃣ Save Data (`main`)
- Save the cleaned data to a new CSV file
- Process:
  - Export DataFrame to CSV
  - Log completion of data cleaning process

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

| Column Name              | Description                                                   | Expected Values                                     |
| ------------------------ | ------------------------------------------------------------- | --------------------------------------------------- |
| `date_submitted`         | Review submission date                                        | "YYYY-MM-DD" (e.g., "2025-03-19")                   |
| `customer_name`          | Name of the reviewer                                          | String (e.g., "John Smith")                         |
| `nationality`            | Reviewer's nationality                                        | String without parentheses (e.g., "United Kingdom") |
| `verify`                 | Verification status                                           | Boolean (True/False)                                |
| `review_body`            | Review content                                                | String without verification text                    |
| `aircraft`               | Aircraft type                                                 | String (standardized format, e.g., "Boeing 777-300") |
| `type_of_traveller`      | Traveler category                                             | String (e.g., "Business", "Leisure")                |
| `seat_type`              | Class of service                                              | String (e.g., "Business Class", "Economy")          |
| `date_flown`             | Flight date                                                   | "YYYY-MM-DD" (e.g., "2025-03-01")                   |
| `seat_comfort`           | Rating for seat comfort                                       | Integer (1-5) or NaN                                |
| `cabin_staff_service`    | Rating for cabin staff service                                | Integer (1-5) or NaN                                |
| `food_and_beverages`     | Rating for food and beverages                                 | Integer (1-5) or NaN                                |
| `inflight_entertainment` | Rating for inflight entertainment                             | Integer (1-5) or NaN                                |
| `ground_service`         | Rating for ground service                                     | Integer (1-5) or NaN                                |
| `wifi_and_connectivity`  | Rating for WiFi and connectivity                              | Integer (1-5) or NaN                                |
| `value_for_money`        | Rating for value                                              | Integer (1-5) or NaN                                |
| `recommended`            | Whether the flight was recommended                            | Boolean (True/False)                                |
| `origin_city`            | Origin city name                                              | String (e.g., "London")                             |
| `origin_airport`         | Origin airport IATA code                                      | String (e.g., "LHR")                                |
| `destination_city`       | Destination city name                                         | String (e.g., "New York")                           |
| `destination_airport`    | Destination airport IATA code                                 | String (e.g., "JFK")                                |
| `transit_city`           | Transit city name (if applicable)                             | String or None                                      |
| `transit_airport`        | Transit airport IATA code (if applicable)                     | String or None                                      |
