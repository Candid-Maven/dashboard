import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import calendar

def generate_daily_utm_supplier_chart(supplier, df):
    # Create a working copy
    df_converted = df.copy()

    if supplier == 'All':
        # Calculate the sum of variables for each date across all suppliers
        df_sum = df_converted.groupby('Date').sum().reset_index()
        supplier_label = 'All'
    else:
        # Filter data for the selected supplier
        df_filtered = df_converted[df_converted['Supplier'] == supplier].copy()

        # Calculate the sum of variables for each date
        df_sum = df_filtered.groupby('Date').sum().reset_index()
        supplier_label = supplier

    # Set up the figure
    fig = go.Figure()

    # Create traces for Reg of the selected supplier
    fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum['Reg'], name=f'Reg'))

    # Create traces for Distinct_Schools, Accepted, and Rejected of the selected supplier
    variables = ['Distinct_Schools', 'Accepted', 'Rejected']
    colors = ['blue', 'green', 'red']

    for variable, color in zip(variables, colors):
        fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum[variable],
                                 name=f'{variable}', yaxis='y2', line=dict(color=color)))

    # Set the layout of the figure
    fig.update_layout(
        title=f'UTM Performance of: {supplier}',
        xaxis=dict(title='Week'),
        yaxis=dict(title='Registrations'),
        yaxis2=dict(title='Acceptance, Rejection', overlaying='y', side='right'),
        plot_bgcolor='#F5F5F5',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def generate_daily_utm_ad_chart(utm_ad_id, df):
    if utm_ad_id == -1:
        ad_label = 'All Ads'
        df_filtered = df.copy()  # No filter applied for 'All Ads'
    else:
        ad_label = f'Ad: {utm_ad_id}'
        df_filtered = df[df['UTM_Ad_Id'] == utm_ad_id].copy()

    # Sum the totals for each value based on the date
    df_sum = df_filtered.groupby('Date').sum().reset_index()

    # Set up the figure
    fig = go.Figure()

    # Create traces for Reg of the selected ad_label or all suppliers
    fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum['Reg'], name=f'Reg'))

    # Create traces for Distinct_Schools, Accepted, and Rejected
    variables = ['Distinct_Schools', 'Accepted', 'Rejected']
    colors = ['blue', 'green', 'red']

    for variable, color in zip(variables, colors):
        fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum[variable],
                                 name=f'{variable}', yaxis='y2', line=dict(color=color)))

    # Set the layout of the figure
    fig.update_layout(
        title=f"UTM Performance of Ad ID: {ad_label}",
        xaxis=dict(title='Week'),
        yaxis=dict(title='Registrations'),
        yaxis2=dict(title='Acceptance, Rejection', overlaying='y', side='right'),
        plot_bgcolor='#F5F5F5',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def generate_weekly_utm_supplier_chart(supplier, df):
    # Create a working copy
    df_converted = df.copy()

    if supplier == 'All':
        # Calculate the sum of variables for each date across all suppliers
        df_sum = df_converted.groupby('Date').sum().reset_index()
        supplier_label = 'All'
    else:
        # Filter data for the selected supplier
        df_filtered = df_converted[df_converted['Supplier'] == supplier].copy()

        # Calculate the sum of variables for each date
        df_sum = df_filtered.groupby('Date').sum().reset_index()
        supplier_label = supplier

    # Set up the figure
    fig = go.Figure()

    # Create traces for Reg of the selected supplier
    fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum['Reg'], name=f'Reg'))

    # Create traces for Distinct_Schools, Accepted, and Rejected of the selected supplier
    variables = ['Distinct_Schools', 'Accepted', 'Rejected']
    colors = ['blue', 'green', 'red']

    for variable, color in zip(variables, colors):
        fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum[variable],
                                 name=f'{variable}', yaxis='y2', line=dict(color=color)))

    # Set the layout of the figure
    fig.update_layout(
        title=f'UTM Performance of: {supplier}',
        xaxis=dict(title='Week'),
        yaxis=dict(title='Registrations'),
        yaxis2=dict(title='Acceptance, Rejection', overlaying='y', side='right'),
        plot_bgcolor='#F5F5F5',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def generate_weekly_utm_ad_chart(utm_ad_id, df):
    if utm_ad_id == -1:
        ad_label = 'All Ads'
        df_filtered = df.copy()  # No filter applied for 'All Ads'
    else:
        ad_label = f'Ad: {utm_ad_id}'
        df_filtered = df[df['UTM_Ad_Id'] == utm_ad_id].copy()

    # Sum the totals for each value based on the date
    df_sum = df_filtered.groupby('Date').sum().reset_index()

    # Set up the figure
    fig = go.Figure()

    # Create traces for Reg of the selected ad_label or all suppliers
    fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum['Reg'], name=f'Reg'))

    # Create traces for Distinct_Schools, Accepted, and Rejected
    variables = ['Distinct_Schools', 'Accepted', 'Rejected']
    colors = ['blue', 'green', 'red']

    for variable, color in zip(variables, colors):
        fig.add_trace(go.Scatter(x=df_sum['Date'], y=df_sum[variable],
                                 name=f'{variable}', yaxis='y2', line=dict(color=color)))

    # Set the layout of the figure
    fig.update_layout(
        title=f"UTM Performance of ID: {ad_label}",
        xaxis=dict(title='Week'),
        yaxis=dict(title='Registrations'),
        yaxis2=dict(title='Acceptance, Rejection', overlaying='y', side='right'),
        plot_bgcolor='#F5F5F5',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig