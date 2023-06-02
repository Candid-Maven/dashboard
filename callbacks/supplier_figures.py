import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import calendar

def generate_daily_supplier_chart(supplier, df):
    if 'All' == supplier:
        df_filtered = df.groupby('Date')['Count'].sum().reset_index()
    else:
        # Filter to the selected supplier
        df_filtered = df[df['Supplier'] == supplier].reset_index()

    # Find average count by supplier
    average_counts = df_filtered['Count'].mean()

    # Get the start and end dates for the first week and second week
    first_week_start = df_filtered['Date'].min()
    first_week_end = first_week_start + pd.DateOffset(days=6)

    second_week_start = first_week_end + pd.DateOffset(days=1)
    second_week_end = df_filtered['Date'].max()

    # Create dataframes for the first week and second week
    df_first_week = df_filtered[(df_filtered['Date'] >= first_week_start) & (df_filtered['Date'] <= first_week_end)].reset_index()
    df_second_week = df_filtered[(df_filtered['Date'] >= second_week_start) & (df_filtered['Date'] <= second_week_end)]

    # Create the figure
    fig = go.Figure()

    # Plot the first week data on x-axis with color #323232
    fig.add_trace(go.Scatter(x=df_first_week['Date'], y=df_first_week['Count'], mode='lines', name='{} - {}'.format(first_week_start.date(), first_week_end.date()), line_color='#323232'))

    fig.add_shape(type='line', x0=df_first_week['Date'].min(), x1=df_first_week['Date'].max(),
                  y0=average_counts, y1=average_counts, line=dict(color='#646464', dash='dash'))

    # Plot the second week data on x-axis2 with color #2541B2
    fig.add_trace(go.Scatter(x=df_second_week['Date'], y=df_second_week['Count'], mode='lines', name='{} - {}'.format(second_week_start.date(), second_week_end.date()),
                             line=dict(color='#2541B2'), xaxis='x2'))

    # Set the layout properties
    fig.update_layout(
        title='Total Counts by: {}'.format(supplier),
        xaxis=dict(title='Date', color='#323232', range=[first_week_start, first_week_end]),
        xaxis2=dict(showticklabels=False, range=[second_week_start, second_week_end], overlaying='x'),
        yaxis=dict(title='Total Counts'),
        legend=dict(x=0, y=1, bgcolor='rgba(255, 255, 255, 0.5)', xanchor='left', yanchor='top'),
        plot_bgcolor='#F5F5F5'
    )

    return fig

def generate_supplier_comparison_chart(df):

    # Sort the DataFrame by the 'First Week' column in ascending order
    df = df.sort_values('First Week', ascending=True)
    
    # Create the bar chart in Plotly
    suppliers = df.index
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['First Week'], y=suppliers, name= "Last Week", marker_color='#323232', orientation='h'))
    fig.add_trace(go.Bar(x=df['Second Week'], y=suppliers, name='This Week', marker_color='blue', orientation='h'))
   
    fig.update_layout(
        title='Total Counts by Supplier',
        xaxis_title='Total Counts',
        yaxis_title='Supplier',
        barmode='group',
        plot_bgcolor='#F5F5F5'
    )

    return fig

def generate_weekly_volume_chart(supplier, df):
    # Create a Plotly Figure
    fig = go.Figure()

    if 'All' == supplier:
        df_filtered = df.groupby('Year-Week')['Count'].sum().reset_index()
    else:
        # Filter the df to the selected supplier
        df_filtered = df[df['Supplier'] == supplier]

    # SQL query provides Year-Week data in ISO %Y-%U format, currently a string. Convert to datetime.
    def convert_year_week(year_week):
        year, week = map(int, year_week.split('-'))
        # Assuming Monday as the day of the week
        return datetime.datetime.strptime(f'{year}-{week}-1', '%Y-%W-%w')

    df_filtered.loc[:, 'Year-Week'] = df_filtered['Year-Week'].apply(convert_year_week)
    df_filtered['Year-Week'] = pd.to_datetime(df_filtered['Year-Week'])

    start_month = df_filtered['Year-Week'].iloc[0].month
    end_month = df_filtered['Year-Week'].iloc[-1].month
    num_months = (end_month - start_month + 1) % 12  # Calculate the number of months

    if num_months > 5:
        start_month = (start_month + 1) % 12
        num_months -= 1

    df_monthly = []

    for month in range(start_month, start_month + num_months):
        current_month = (month - 1) % 12 + 1  # Calculate the current month within a year
        start_date = df_filtered[df_filtered['Year-Week'].dt.month == current_month].iloc[0]['Year-Week'] - pd.DateOffset(weeks=1)
        end_date = df_filtered[df_filtered['Year-Week'].dt.month == current_month].iloc[-1]['Year-Week'] + pd.DateOffset(weeks=1)
        df_monthly.append(df_filtered[(df_filtered['Year-Week'] >= start_date) & (df_filtered['Year-Week'] <= end_date)])

    # print(df_monthly)
    color_range = ["#808080", "#505050", "#282828", '#161616', '#2541B2']

    date_ranges = []

    for i in range(num_months):
        fig.add_trace(
            go.Scatter(
              x=df_monthly[i]['Year-Week'],
              y=df_monthly[i]['Count'],
              marker_color=color_range[i],
              xaxis=f"x{i+1}",
              name=df_monthly[i]['Year-Week'].iloc[1].strftime('%b')
            )
        )

        date = df_monthly[i]['Year-Week'].iloc[1]
        date_ranges.append([date.replace(day=1), date.replace(day=calendar.monthrange(date.year, date.month)[1])])

    fig.update_layout(
        title=f"{supplier} Monthly Historical Volume",
        hovermode='closest',
        yaxis=dict(title='Total Weekly Volume', anchor='x', overlaying='x2', range=[df_filtered['Year-Week'].iloc[0], df_filtered['Year-Week'].iloc[-1]]),
        legend=dict(yanchor='top', y=.99, xanchor='left', x=.01),
        plot_bgcolor='#F5F5F5',
        xaxis1=dict(anchor='x1', overlaying='x5', range=date_ranges[0], showticklabels=False),
        xaxis2=dict(anchor='x2', overlaying='x5', range=date_ranges[1], showticklabels=False),
        xaxis3=dict(anchor='x3', overlaying='x5', range=date_ranges[2], showticklabels=False),
        xaxis4=dict(anchor='x4', overlaying='x5',range=date_ranges[3], showticklabels=False),
        xaxis5=dict(title='Week', anchor='x5', range=date_ranges[4]),
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