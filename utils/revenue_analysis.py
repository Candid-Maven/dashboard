import pandas as pd
import numpy as np
import datetime as dt

def daily_analysis(df):
    # Convert the `date` column to datetime type
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")

    # Round the timestamps to the nearest day
    df['date'] = df['date'].dt.floor('D')

    # Get today's date
    today = pd.to_datetime("today").date()

    # Calculate the start and end dates for the 28-day period
    end_date = pd.to_datetime("today").normalize() - pd.Timedelta(days=1)
    start_date = end_date - pd.Timedelta(days=27)

    # Filter the data to only include dates within the 28-day period
    df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Group the data by source and date, and sum the revenue
    df_grouped = df_filtered.groupby(["source", "date"])["revenue"].sum().reset_index()

    # Pivot the data so that each source is a column and each date is a row
    df_pivoted = df_grouped.pivot(index="source", columns="date", values="revenue")

    # Replace any NaN values with 0
    df_pivoted = df_pivoted.fillna(0)

    return [df_pivoted, today]


def weekly_analysis(df):
    # Convert the `date` column to datetime type
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")

    # Get today's date
    today = pd.to_datetime("today")

    # Calculate dates based on today's date
    dates = []
    for i in range(8):
        start_date = today - dt.timedelta(days=7 * (i + 1))
        end_date = today - dt.timedelta(days=7 * i)
        dates.append((start_date, end_date))

    # Get weekly revenue by source using filters
    weekly_revenue_by_source = {}
    for i, (start_date, end_date) in enumerate(dates):
        weekly_revenue_by_source[i + 1] = (
            df[(df["date"] >= start_date) & (df["date"] < end_date)]
            .groupby("source")["revenue"]
            .sum()
        )
        
    # Get the average revenue for the previous two four-week periods (excluding current week)
    average_recent_weekly_revenue_by_source = sum(weekly_revenue_by_source[i] for i in range(2, 5)) / 3
    average_previous_weekly_revenue_by_source = sum(weekly_revenue_by_source[i] for i in range(5, 9)) / 4

    # Merge historical data into a single dataframe
    revenue_by_source = pd.concat(
        [weekly_revenue_by_source[i + 1] for i in range(8)]
        + [
            average_recent_weekly_revenue_by_source,
            average_previous_weekly_revenue_by_source,
        ],
        axis=1,
        keys=[
            "last_week_revenue",
            "two_week_revenue",
            "three_week_revenue",
            "four_week_revenue",
            "five_week_revenue",
            "six_week_revenue",
            "seven_week_revenue",
            "eight_week_revenue",
            "recent_weekly_average",
            "previous_weekly_average",
        ],
    )

    # Fill in any missing values with 0
    revenue_by_source.fillna(0, inplace=True)

    # Sort the DataFrame by last week's revenue
    revenue_by_source = revenue_by_source.sort_values(
        by="last_week_revenue", ascending=False
    )

    return [revenue_by_source, today]


def cumulative_analysis(df):
    # Convert the `date` column to datetime type
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")

    # Get today's date
    today = pd.to_datetime('today')

    # Calculate the start for the current month and the previous month
    start_of_current_month = today.replace(day=1)
    start_of_previous_month = (today - pd.DateOffset(months=1)).replace(day=1)
    print(start_of_previous_month)

    # Filter the data to each month
    df_last_month = df[(df['date'] > start_of_previous_month - pd.DateOffset(days=1)) & (df['date'] < start_of_current_month - pd.DateOffset(days=1))]
    df_this_month = df[(df['date'] > start_of_current_month - pd.DateOffset(days=1)) & (df['date'] <= today)]

    # Group the data by source and date, and sum the revenue using pd.Grouper
    df_last_grouped = df_last_month.groupby(['source', pd.Grouper(key='date', freq='D')])['revenue'].sum().reset_index()
    df_this_grouped = df_this_month.groupby(['source', pd.Grouper(key='date', freq='D')])['revenue'].sum().reset_index()

    # Pivot the data so that each source is a column and each date is a row
    df_last_pivoted = df_last_grouped.pivot(index='source', columns='date', values='revenue').fillna(0)
    df_this_pivoted = df_this_grouped.pivot(index='source', columns='date', values='revenue').fillna(0)

    # Get the cumulative sum for each month
    df_last_cumulative = df_last_pivoted.cumsum(axis=1)
    df_this_cumulative = df_this_pivoted.cumsum(axis=1)

    return [df_last_cumulative, df_this_cumulative, today]