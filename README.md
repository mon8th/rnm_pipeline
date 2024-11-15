Rick and Morty Data ETL Pipeline

This project extracts, transforms, and loads (ETL) data from the Rick and Morty API. The data includes characters, locations, and episodes from the show, which are processed and stored in an SQLite database.

Project Structure

/files
    ├── cleaned_data.json  # The cleaned data ready for transformation
    ├── combined_data.csv # The final output in CSV format
    ├── raw_data.json     # The raw data extracted from the API
    └── rnm.db            # The SQLite database where the final data is stored
/rnm_pipeline.py           # The ETL script
Requirements

To run this pipeline, you need Python installed along with the following packages:

pandas
requests
json
sqlite3
You can install the necessary packages using pip:

pip install pandas requests
SQLite is bundled with Python, so no additional installation is needed for it.

How to Use

1. Clone the Repository
To get started, clone the repository to your local machine:

git clone https://github.com/mon8th/rnm_pipeline.git
cd rnm_pipeline
2. Run the ETL Script
Run the rnm_pipeline.py script to fetch data from the API, clean and transform it, and store it in an SQLite database.

python rnm_pipeline.py
This will:

Fetch data from the Rick and Morty API.
Clean and transform the data.
Store the cleaned data in cleaned_data.json and the final data in combined_data.csv.
Insert the processed data into an SQLite database rnm.db.
3. Check the Results
Database: You can view the data inside rnm.db using a database management tool like DB Browser for SQLite or TablePlus.
CSV File: Open combined_data.csv to see the data in a tabular format.
