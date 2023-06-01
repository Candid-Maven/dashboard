import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_daily_utm(df):
    # Create a working copy
    df_converted = df.copy()

    # Fill NaN values with 0 in specified columns
    columns_to_fill = ['Reg', 'Distinct_Schools', 'Accepted', 'Rejected', 'Rev', 'CPA']
    df_converted[columns_to_fill] = df_converted[columns_to_fill].fillna(0)

    # Fill NaN values with 'Unknown' in specified columns
    columns_to_fill = ['UTM_Ad_Id', 'Supplier']
    df_converted[columns_to_fill] = df_converted[columns_to_fill].fillna('Unknown')

    # Sort the dataframe by date
    df_converted = df_converted.sort_values('Date')

    return df_converted

def analyze_weekly_utm(df):
    # Create a working copy
    df_converted = df.copy()

    # Convert 'Year-Week' to date
    df_converted['Year-Week'] = df_converted['Year-Week'].astype(str)
    df_converted['Date'] = df_converted['Year-Week'].apply(lambda x: datetime.strptime(x + '-1', "%Y%W-%w"))

    # Find the minimum date
    min_date = df_converted['Date'].min()

    # Exclude the earliest data based on the minimum date
    df_converted = df_converted[df_converted['Date'] > min_date]

    # Fill NaN values with 0 in specified columns
    columns_to_fill = ['Reg', 'Distinct_Schools', 'Accepted', 'Rejected', 'Rev', 'CPA']
    df_converted[columns_to_fill] = df_converted[columns_to_fill].fillna(0)

    # Fill NaN values with 'Unknown' in specified columns
    columns_to_fill = ['UTM_Ad_Id', 'Supplier']
    df_converted[columns_to_fill] = df_converted[columns_to_fill].fillna('Unknown')

    return df_converted

def analyze_weekly_top_ad(df):
    # Filter the data to look at the last 10 days
    last_week = datetime.now() - timedelta(days=7)
    df['Date'] = pd.to_datetime(df['Date'])
    df_filtered = df[df['Date'] >= last_week]

    # Define the predictor variables
    predictor_variables = ['Site_Name', 'UTM_Source', 'UTM_Campaign', 'UTM_Supplier_Id', 'UTM_Ad_Id', 'UTM_Content', 'Supplier']

    # Define the outcome variables
    outcome_variables = ['Reg', 'Accepted', 'Rejected', 'Rev']

    # Calculate the mean values of the outcome variables for each combination of predictors
    mean_outcomes = df.groupby(predictor_variables)[outcome_variables].mean().reset_index()

    winner = mean_outcomes.groupby('UTM_Ad_Id')['Reg'].mean().nlargest(1)

    return winner.index[0]

def analyze_weekly_bottom_ad(df):
    # Filter the data to look at the last week
    last_week = datetime.now() - timedelta(days=7)
    df['Date'] = pd.to_datetime(df['Date'])
    df_filtered = df[df['Date'] >= last_week]

    # Define the predictor variables
    predictor_variables = ['Site_Name', 'UTM_Source', 'UTM_Campaign', 'UTM_Supplier_Id', 'UTM_Ad_Id', 'UTM_Content', 'Supplier']

    # Define the outcome variables
    outcome_variables = ['Reg', 'Accepted', 'Rejected', 'Rev']

    # Calculate the mean values of the outcome variables for each combination of predictors
    mean_outcomes = df.groupby(predictor_variables)[outcome_variables].mean().reset_index()

    loser = mean_outcomes.groupby('UTM_Ad_Id')['Reg'].mean().nsmallest(1)

    return loser.index[0]