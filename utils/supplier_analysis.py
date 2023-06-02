import pandas as pd
import numpy as np
import datetime as dt

def daily_supplier_counts(df):
    # Convert the index to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Group the data by date and supplier, summing the counts
    df_grouped = df.groupby(['Date', 'Supplier'])['Count'].sum().reset_index()

    # Create a date range from the minimum to maximum date in the dataframe
    date_range = pd.date_range(df_grouped['Date'].min(), df_grouped['Date'].max(), freq='D')

    # Create a multi-index with all combinations of dates and suppliers
    multi_index = pd.MultiIndex.from_product([date_range, df_grouped['Supplier'].unique()], names=['Date', 'Supplier'])

    # Reindex the dataframe with the multi-index
    df_reindexed = df_grouped.set_index(['Date', 'Supplier']).reindex(multi_index, fill_value=0).reset_index()

    return df_reindexed

def compare_suppliers(df):
    # Convert the "Date" column to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Determine the start and end dates for the first and second weeks
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    mid_date = min_date + pd.DateOffset(days=7)

    # Filter and aggregate the data for the first week
    first_week_df = df[df['Date'] < mid_date]
    first_week_counts = first_week_df.groupby('Supplier')['Count'].sum()
    first_week_total = first_week_counts.sum()

    # Add the first week total as a key-value pair in the first week counts DataFrame
    first_week_counts['Total'] = first_week_total

    # Filter and aggregate the data for the second week
    second_week_df = df[df['Date'] >= mid_date]
    second_week_counts = second_week_df.groupby('Supplier')['Count'].sum()
    second_week_total = second_week_counts.sum()

    # Add the second week total as a key-value pair in the second week counts DataFrame
    second_week_counts['Total'] = second_week_total

    # Combine the first and second week counts DataFrames
    combined_df = pd.concat([first_week_counts, second_week_counts], axis=1, keys=['First Week', 'Second Week']).fillna(0)

    return combined_df

def weekly_supplier_volume(df):
    # Aggregate the total count for each supplier
    df_supplier_counts = df.groupby(['Year-Week', 'Supplier'])['Count'].sum().reset_index()  
    return df_supplier_counts