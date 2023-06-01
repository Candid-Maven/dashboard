import os
import sys
import pandas as pd
import pymysql
import json

def get_secrets():
    if os.getenv('GITHUB_ACTIONS') == 'true':
        # Running in GitHub Actions, retrieve secrets from GitHub secrets
        PORTAL_USERNAME = os.getenv('GITHUB_PORTAL_USERNAME')
        PORTAL_PASSWORD = os.getenv('GITHUB_PORTAL_PASSWORD')
    elif os.getenv('HEROKU') == 'true' or os.getenv('DEPLOYMENT_ENV') == 'production':
        # Running on Heroku, retrieve secrets from environment variables
        PORTAL_USERNAME = os.getenv('PORTAL_USERNAME')
        PORTAL_PASSWORD = os.getenv('PORTAL_PASSWORD')
    else:
        # Running locally, retrieve secrets from local file
        sys.path.append(os.path.join(os.getcwd(), 'config'))
        from my_secrets import PORTAL_USERNAME, PORTAL_PASSWORD
    
    return PORTAL_USERNAME, PORTAL_PASSWORD

# Get the secrets based on the execution environment
PORTAL_USERNAME, PORTAL_PASSWORD = get_secrets()

def fetch_data():
    # Define database connection values
    REGION = 'us-west-2'
    endpoint = 'cm-mysql-db1.clnzezx2g6fi.us-west-2.rds.amazonaws.com'
    username = PORTAL_USERNAME
    password = PORTAL_PASSWORD
    db_name = 'portal'
    port = 3306
    timeout = 10

    # Add the directory to sys.path
    query_dir = os.path.join(os.getcwd(), 'data', 'queries', 'supplier')
    sys.path.append(query_dir)

    # Get a list of all the SQL query files in the directory
    query_files = [os.path.join(query_dir, f) for f in os.listdir(query_dir) if f.endswith('.sql')]

    #Connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=db_name, connect_timeout=timeout)

    # Define an empty dictionary to store the results dataframes
    results = {}

    # Loop through the query files, execute each query, and store the results dataframe in the dictionary
    for query_file in query_files:
        with open(query_file, 'r') as f:
            sql = f.read()

        # Extract the name of the file (without the .sql extension) to use as the dataframe name
        df_name = os.path.splitext(os.path.basename(query_file))[0]
        df_name = f'df_{df_name}' # Add prefix to the dataframe name

        # Execute the query and store the results dataframe in the dictionary
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            df = pd.DataFrame.from_records(rows, columns=columns)
            results[df_name] = df

    # print('Queries completed')

    # Close connection.
    connection.close()

    # Set the directory to save the CSV files
    output_dir = os.path.join(os.getcwd(), 'data', 'raw_data', 'supplier')
    sys.path.append(output_dir)

    # Iterate over each DataFrame in the dictionary
    for key, df in results.items():
        # Create the path to the output CSV file
        output_file = os.path.join(output_dir, f"{key}.csv")
        
        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False)
    
#     print('Raw files saved')
# fetch_data()

def clean_data():
    # Set the directory to load the CSV files
    input_dir = os.path.join(os.getcwd(), 'data', 'raw_data', 'supplier')
    sys.path.append(input_dir)

    # Initialize an empty dictionary to store the loaded DataFrames
    loaded_data = {}

    # Iterate over each file in the input directory and filter only CSV files
    for file in [f for f in os.listdir(input_dir) if f.endswith('.csv')]:
        # Get the key name from the filename by removing the '.csv' extension
        key = os.path.splitext(file)[0]

        # Load the CSV file into a DataFrame and store it in the dictionary
        df = pd.read_csv(os.path.join(input_dir, file))
        loaded_data[key] = df

    # print('Raw files loaded')

    #setting names of dataframes
    df_supplier_weekly_volume = loaded_data['df_supplier_weekly_volume']
    df_supplier_daily_volume = loaded_data['df_supplier_daily_volume']
    df_boom = loaded_data['df_boom']
    df_zealous = loaded_data['df_zealous']

    # save processed data to new file
    output_dir = os.path.join(os.getcwd(), 'data', 'processed_data')
    sys.path.append(output_dir)

    output_file = os.path.join(output_dir, 'supplier_weekly.csv')
    df_supplier_weekly_volume.to_csv(output_file, index=False)

    output_file = os.path.join(output_dir, 'supplier_daily.csv')
    df_supplier_daily_volume.to_csv(output_file, index=False)

    output_file = os.path.join(output_dir, 'boom.csv')
    df_boom.to_csv(output_file, index=False)

    output_file = os.path.join(output_dir, 'zealous.csv')
    df_zealous.to_csv(output_file, index=False)

#     print('Clean files saved')
# clean_data()

def load_data(file):
    # save processed data to new file
    input_dir = os.path.join(os.getcwd(), 'data', 'processed_data')
    sys.path.append(input_dir)
    input_file = os.path.join(input_dir, file + '.csv')

    # Create empty dictionary for dataframe
    df = {}

    # Read .csv file and save to dataframe
    df = pd.read_csv(input_file)

    return df