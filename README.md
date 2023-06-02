# Dashboard
This dashboard shows operational data for Candid Maven.com


## File structure

## Components
### Revenue Fetch
* fetch_data()
  * Inputs: none
  * Outputs: none
  * Uses username and password for ELMS database from my_secrets.py
  * Uses SQL queries from /data/queries/revenue
  * Completes fetch requests using queries to pull data from ELMS database
  * Converts raw data into dataframes
  * Saves raw data as .csv files in /data/raw_data

* clean_data()
  * Inputs: none
  * Outputs: none
  * Uses raw data from .csv files in /data/raw_data
  * Establishes the source for each entry
  * Replaces NaN in campaign with 'Unknown'
  * Replaces NaN in click_count with 0
  * Standardizes date with hourly fidelity
  * Saves processed data as revenue.csv in /data/processed_data

* load_data()
  * Inputs: none
  * Outputs: composite dataframe of processed revenue data
  * Opens the .csv cached data for processed revenue
  * Exports the dataframe for use

### Revenue Analysis
* daily_analysis()
  * Inputs: composite dataframe of processed revenue data
  * Outputs: an array containing:
    * Revenue for each day
    * A value for today's date
  * Calculates today and the days of the week ending today
  * Processes the dataframe to group by source and date, creating a total for each source in a given day
  * Fills any blanks with 0
* weekly_analysis()
  * Inputs: composite dataframe of processed revenue data
  * Outputs: an array containing:
    * Revenue for each week
    * Reference date for today
  * Calculates today and start points for the previous eight weeks
  * Processes the dataframe to group by source within date ranges for each week, creating a total revenue for each source in a given week
  * Calculates the average revenue for each four-week period
  * Merges data into a single dataframe for export
  * Fills blanks with 0
* cumulative_analysis()
  * Inputs: composite dataframe of processed revenue data
  * Outputs: an array containing:
    * Cumulative revenue for each day within last month
    * Cumulative revenue for each day within this month
    * A value for today's day
  * Calculates today and the beginning of the current and previous month
  * Processes the dataframe to group by source and date, creating a total for each source in a given day
  * Fills any blanks with 0
  * Performs the cumulative sum for a given month: months begin on the 15th

### Revenue Figures
* generate_weekly_chart
* generate_daily_chart
* generate_cumulative_chart

### 

## Configuration Setup

## Dependencies
