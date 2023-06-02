import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta
from plotly.subplots import make_subplots
import calendar

def generate_daily_chart(company, revenue_by_day, today):
    # Create a Plotly figure
    fig = go.Figure()

    if 'All' == company:
        revenue_by_day = revenue_by_day.sum(axis=0).reset_index().transpose()
        index = 1
    else:
        # Find the row index for the selected company
        index = revenue_by_day.index.get_loc(company)

    # Create an array of the days of the week, ending with today
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    today_weekday = today.strftime("%A")
    x_labels = (
        days_of_week[days_of_week.index(today_weekday) :]
        + days_of_week[: days_of_week.index(today_weekday)]
    )

    # Create a range of colors for progressively increasing boldness
    color_range = ["#808080", "#505050", "#282828", "#161616"]

    for i in range(3):
        fig.add_trace(
            go.Scatter(
                x=x_labels,
                y=revenue_by_day.iloc[index][0 + i * 7:7 + i * 7],
                name=str(3-i) + " weeks ago",
                marker_color=color_range[i],
                hovertext=[
                    f"Date: {date}<br>Revenue: ${revenue:.2f}"
                    for date, revenue in zip(
                        revenue_by_day.columns[0 + i * 7:7 + i * 7],
                        revenue_by_day.iloc[index][0 + i * 7:7 + i * 7]
                    )
                ],
                hovertemplate="%{hovertext} <extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=x_labels,
            y=revenue_by_day.iloc[index][21:28],
            name="This week",
            marker_color="#2541B2",
            hovertext=[
                f"Date: {date}<br>Revenue: ${revenue:.2f}"
                for date, revenue in zip(
                    revenue_by_day.columns[21:28],
                    revenue_by_day.iloc[index][21:28]
                )
            ],
            hovertemplate="%{hovertext} <extra></extra>",
        )
    )

    # Update the layout
    fig.update_layout(
        title=f"Revenue by day: {company}",
        legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
        xaxis_title="Day",
        yaxis_title="Revenue",
        plot_bgcolor="#F5F5F5",
        yaxis_tickprefix='$',
    )

    return fig

def generate_weekly_chart(company, revenue_by_source, today):
    if 'All' == company:
        revenue_by_source.loc['All'] = revenue_by_source.sum()  # Add a new row for 'All' with the sum of all rows
        index = revenue_by_source.index.get_loc('All')
    else:
        index = revenue_by_source.index.get_loc(company)

    # Create the figure
    fig = go.Figure()

    # Calculate dates based on today's date
    dates = []
    for i in range(8):
        start_date = today - timedelta(weeks=(i + 1))
        end_date = today - timedelta(weeks=i)
        dates.append((start_date, end_date))

    # Define x-axis labels
    date_strings = [
        f"{start.strftime('%B %d')} to {end.strftime('%B %d')}" for start, end in dates
    ]

    # Plot the last four weeks in blue
    fig.add_trace(
        go.Scatter(
            x=date_strings[3::-1],
            y=[
                revenue_by_source.iloc[index]['four_week_revenue'],
                revenue_by_source.iloc[index]['three_week_revenue'],
                revenue_by_source.iloc[index]['two_week_revenue'],
                revenue_by_source.iloc[index]['last_week_revenue'],
            ],
            name='Recent 4-Week Period',
            line=dict(color="blue", width=2),
        )
    )

    # Add a horizontal line for the three-week average revenue
    fig.add_trace(
        go.Scatter(
            x=[date_strings[3], date_strings[0]],
            y=[revenue_by_source.iloc[index]['recent_weekly_average']] * 2,
            name='Recent 3-Week Average',
            line=dict(color="yellow", width=2, dash="dash"),
        )
    )

    # Plot the overlapping four weeks in gray
    fig.add_trace(
        go.Scatter(
            x=date_strings[7:3:-1],
            y=[
                revenue_by_source.iloc[index]['eight_week_revenue'],
                revenue_by_source.iloc[index]['seven_week_revenue'],
                revenue_by_source.iloc[index]['six_week_revenue'],
                revenue_by_source.iloc[index]['five_week_revenue'],
            ],
            name='Previous 4-Week Period',
            line=dict(color="#161616", width=2),
            xaxis='x2',
            yaxis='y'
        )
    )

    # Add a horizontal line for the four-week average revenue
    fig.add_trace(
        go.Scatter(
            x=[date_strings[7], date_strings[4]],
            y=[revenue_by_source.iloc[index]['previous_weekly_average']] * 2,
            name='Previous 4-Week Average',
            line=dict(color="#808080", width=2, dash="dash"),
            xaxis='x2',
            yaxis='y'
        )
    )

    # Set the layout for the figure
    fig.update_layout(
        title=f"Weekly Trends: {company}",
        legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
        xaxis=dict(title="Week"),
        yaxis=dict(title="Revenue"),
        yaxis_tickprefix='$',
        xaxis2=dict(
            showticklabels=False,
            anchor="x2",
            overlaying="x",
        ),
        plot_bgcolor="#F5F5F5",
    )

    return fig

def generate_cumulative_chart(company, last_month_revenue, this_month_revenue, today):
    # Create a new figure
    fig = go.Figure()

    if 'All' == company:
        last_month_revenue.loc['All'] = last_month_revenue.sum()  # Add a new row for 'All' with the sum of all rows
        index = last_month_revenue.index.get_loc('All')
        this_month_revenue.loc['All'] = this_month_revenue.sum()  # Add a new row for 'All' with the sum of all rows
        index = this_month_revenue.index.get_loc('All')
    else: 
        # Find the row index for the selected company
        index = this_month_revenue.index.get_loc(company)
        index2 = last_month_revenue.index.get_loc(company)

    # Get the start and end dates of the current month
    start_date = today.replace(day=1)
    end_date = start_date + pd.offsets.MonthEnd(1)

    # Get the start and end dates of last month
    start_date2 = (today - pd.DateOffset(months=1)).replace(day=1)
    end_date2 = start_date2 + pd.offsets.MonthEnd(1)

    # Add the traces for this month's revenue
    fig.add_trace(
        go.Scatter(
            x=this_month_revenue.columns,
            y=this_month_revenue.loc[company].values,
            name=f"{company} ({today.strftime('%B')})",
            marker_color="#2541B2",
            xaxis='x',
        )
    )

    # Add the traces for last month's revenue
    fig.add_trace(
        go.Scatter(
            x=last_month_revenue.columns,
            y=last_month_revenue.loc[company].values,
            name=f"{company} ({(today - pd.DateOffset(months=1)).strftime('%B')})",
            marker_color="#505050",
            xaxis='x2',
        )
    )

    # Set the layout
    fig.update_layout(
        title=f"{company} Cumulative Revenue Comparison",
        xaxis=dict(title='Date', anchor='x', overlaying='x2', range=[start_date - pd.DateOffset(days=1), end_date]),
        yaxis=dict(title='Revenue', tickformat='.2s', hoverformat='.2f', tickprefix='$'),
        xaxis2=dict(anchor='x2', side='top', range=[start_date2 - pd.DateOffset(days=1), end_date2], showticklabels=False,),
        legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
        plot_bgcolor='#F5F5F5',
    )

    return fig

def generate_daily_comparison(revenue_by_day, today):
    # Create a Plotly figure
    fig = go.Figure()

    # Create an array of the days of the week, ending with today
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    today_weekday = today.strftime("%A")
    x_labels = (
        days_of_week[days_of_week.index(today_weekday) :]
        + days_of_week[: days_of_week.index(today_weekday)]
    )

    for company in revenue_by_day.index:
        fig.add_trace(
            go.Scatter(
                x=x_labels,
                y=revenue_by_day.loc[company][21:28],
                name=f"{company}",
                hovertext=[
                    f"Date: {date}<br>Revenue: ${revenue:.2f}"
                    for date, revenue in zip(
                        revenue_by_day.columns[21:28],
                        revenue_by_day.loc[company][21:28]
                    )
                ],
                hovertemplate="%{hovertext} <extra></extra>",
            )
        )

    # Update the layout
    fig.update_layout(
        title="Daily Revenue Comparison",
        legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99),
        xaxis_title="Day",
        yaxis_title="Revenue",
        plot_bgcolor="#F5F5F5",
        yaxis_tickprefix='$',
    )

    return fig

def generate_monthly_comparison(this_month_revenue, today):
    # Create a new figure
    fig = go.Figure()

    # Get the start and end dates of the current month
    start_date = today.replace(day=1)
    end_date = start_date + pd.offsets.MonthEnd(1)

    # Add the traces for this month's revenue
    for company in this_month_revenue.index:
        fig.add_trace(
            go.Scatter(
                x=this_month_revenue.columns,
                y=this_month_revenue.loc[company].values,
                name=f"{company} ({today.strftime('%B')})",
            )
        )

    # Set the layout
    fig.update_layout(
        title='Cumulative Monthly Revenue Comparison',
        xaxis=dict(title='Date', anchor='x', range=[start_date - pd.DateOffset(days=1), end_date]),
        yaxis=dict(title='Revenue', tickformat='.2s', hoverformat='.2f', tickprefix='$'),
        legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99),
        plot_bgcolor='#F5F5F5',
    )

    return fig

def handle_empty():
    # Handle the case where the selected company has no data in the filtered range
    empty_figure = go.Figure()
    empty_figure.update_layout(
        title='No Data Available',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text='No data available for the selected company within the specified date range.',
                showarrow=False,
                font=dict(size=14)
            )
        ],
        plot_bgcolor='#F5F5F5',
    )

    return empty_figure