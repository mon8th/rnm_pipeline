# **Rick and Morty Data ETL Pipeline**

This project extracts, transforms, and loads (ETL) data from the Rick and Morty API. The data includes characters, locations, and episodes from season 1 to season 5, which are processed and stored in an SQLite database.

### Requirements
To run this pipeline, you need Python installed along with the following packages:

- pandas
- requests
- json
- sqlite3

### How to Use

1. Clone the Repository
To get started, clone the repository to your local machine:
- **git clone https://github.com/mon8th/rnm_pipeline.git**
- **cd rnm_pipeline**
  
2. Run the ETL Script
Run the rnm_pipeline.py script to fetch data from the API, clean and transform it, and store it in an SQLite database.
- **python rnm_pipeline.py**

4. Check the Results
Database: You can view the data inside rnm.db using a database management tool (Personally, I prefer TablePlus)
CSV File: Open combined_data.csv to see the data in a tabular format.
