# -*- coding: utf-8 -*-
import sys
import os
import datetime as dt

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Import components
sys.path.append(os.path.join(os.getcwd(), 'callbacks'))
import callbacks.revenue_figures as revenue_figures
import callbacks.supplier_figures as supplier_figures
import callbacks.utm_figures as utm_figures

sys.path.append(os.path.join(os.getcwd(), 'utils'))
import utils.revenue_fetch as revenue_fetch
import utils.revenue_analysis as revenue_analysis
import utils.supplier_fetch as supplier_fetch
import utils.supplier_analysis as supplier_analysis
import utils.utm_fetch as utm_fetch
import utils.utm_analysis as utm_analysis

external_stylesheets = [
    '/assets/app.css',
    'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap'
]

application = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = application.server

# Access and analyze data for revenue charts
df_revenue = revenue_fetch.load_data()
companies = df_revenue['source'].unique()
revenue_date = df_revenue['date'].max()
[daily_revenue_analyzed, today] = revenue_analysis.daily_analysis(df_revenue)
[weekly_revenue_analyzed, today] = revenue_analysis.weekly_analysis(df_revenue)
[last_month_revenue_cumulative, this_month_revenue_cumulative, today] = revenue_analysis.cumulative_analysis(df_revenue)

# Access and analyze data for supplier charts
df_supplier_daily_volume = supplier_fetch.load_data('supplier_daily')
df_supplier_weekly_volume = supplier_fetch.load_data('supplier_weekly')
supplier_date = df_supplier_daily_volume['Date'].max()
suppliers = df_supplier_daily_volume['Supplier'].unique()

daily_supplier_volume = supplier_analysis.daily_supplier_counts(df_supplier_daily_volume)
weekly_supplier_comparison = supplier_analysis.compare_suppliers(df_supplier_daily_volume)
monthly_supplier_volume = supplier_analysis.weekly_supplier_volume(df_supplier_weekly_volume)

# Access and analyze data for utm charts
df_daily_utm = utm_fetch.load_data('daily_utm')
df_weekly_utm = utm_fetch.load_data('weekly_utm')
utm_date = df_daily_utm['Date'].max()

daily_utm_data = utm_analysis.analyze_daily_utm(df_daily_utm)
weekly_utm_data = utm_analysis.analyze_weekly_utm(df_weekly_utm)
utm_suppliers = weekly_utm_data['Supplier'].unique()
utm_ads = weekly_utm_data['UTM_Ad_Id'].unique()

#  -------we will be moving this to a seperate controller file for refactor-----

# conditionals for the BFNs - All companies weekly
weekly_revenue_difference = weekly_revenue_analyzed['last_week_revenue'].sum() - weekly_revenue_analyzed['previous_weekly_average'].sum()
weekly_color = 'green' if weekly_revenue_difference > 0 else 'red' if weekly_revenue_difference < 0 else 'black'

# -------Logic for all companies daily revenue-------
# setting the date for the second to most recent entry
second_most_recent_date = daily_revenue_analyzed.columns[-1].strftime('%Y-%m-%d')
# returning totaly company revenue on second most recent date
second_recent_data = daily_revenue_analyzed[second_most_recent_date].sum()
# Find the differnce between daily revenue of 2nd and 3rd most recent dates
daily_revenue_difference = daily_revenue_analyzed[daily_revenue_analyzed.columns[-1]].sum() -  daily_revenue_analyzed[daily_revenue_analyzed.columns[-2]].sum()
# setting color of the difference is negative, positive or zero
daily_color = 'green' if daily_revenue_difference > 0 else 'red' if daily_revenue_difference < 0 else 'black'

# Daily count for all suppliers for BFN
# grabbing the most recent full day(yesterday)
latest_date_supplier = sorted(daily_supplier_volume['Date'].unique(), reverse=True)[1].strftime('%Y-%m-%d')
# grabbing the sum of those suppliers count from yesterday
latest_data_sum = daily_supplier_volume.loc[daily_supplier_volume['Date'] == latest_date_supplier, 'Count'].sum()

# Daily difference between the last two days supplier BFN
# Grabbing the second most recent Date(not including the current day we are on)
second_most_recent_day = sorted(daily_supplier_volume['Date'].unique(), reverse=True)[2].strftime('%Y-%m-%d')
second_latest_data_sum = daily_supplier_volume.loc[daily_supplier_volume['Date'] == second_most_recent_date, 'Count'].sum()
supplier_daily_dif = second_latest_data_sum - latest_data_sum
sup_daily_dif_color = 'green' if supplier_daily_dif > 0 else 'red' if supplier_daily_dif < 0 else 'black'

#  Weekly count for all suppliers for BFN
recent_supplier_week_sum = weekly_supplier_comparison['Second Week'].sum()
weekly_supplier_difference =  weekly_supplier_comparison['Second Week'].sum()-weekly_supplier_comparison['First Week'].sum()
supplier_weekly_color = 'green' if weekly_supplier_difference > 0 else 'red' if weekly_supplier_difference < 0 else 'black'

# BFN data for UTM
utm_date = daily_utm_data['Date'].max()
utm_winner = utm_analysis.analyze_weekly_top_ad(df_daily_utm)
utm_loser = utm_analysis.analyze_weekly_bottom_ad(df_daily_utm)

# ====== Start of App Layout===========
application.layout = html.Div([
    html.Img(src='assets/logo.svg', alt='logo'),
    html.H1('Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.H3('Revenue'),
        html.P(f"Latest datum: {revenue_date}"),
        html.P('Select a company:'),
        dcc.Dropdown(
            id='company-dropdown',
            options=[{'label': company, 'value': company} for company in companies],
            value=companies[1],
            className='drop-down'
        )
    ], className='drop-down-grid'),

    html.Div([
        html.Div([
            html.H5(f"All Companies Daily Revenue ({second_most_recent_date}) :"),
            html.H2(f"${'{:,.2f}'.format(second_recent_data)}"),
            html.H3(f"+${daily_revenue_difference:,.2f}", style={'color': daily_color}),
        ],className='bfn-grid'),

        html.Div([
            html.H5('All Companies Weekly Revenue:'),
            html.H2(f"${weekly_revenue_analyzed['last_week_revenue'].sum():,.2f}"),
            html.H3(f"${weekly_revenue_difference:,.2f}", style={'color': weekly_color}),
        ],className='bfn-grid'),

         html.Div([
            html.H5(f"Daily Revenue ({second_most_recent_date}) :"),
            html.H2(id='daily_revenue_bfn'),
            html.H3(id='bfn_daily_difference')
        ],className='bfn-grid'),

        html.Div([
            html.H5('Weekly Revenue:'),
            html.H2(id='bfn_weekly'),
            html.H3(id='bfn_weekly_difference')
        ],className='bfn-grid'),
    ], className='bfn-basic-grid'),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='monthly-revenue-comparison', className='line-chart', figure=revenue_figures.generate_monthly_comparison(this_month_revenue_cumulative, today))])
        ]),

        html.Div([
            html.Div([dcc.Graph(id='monthly-revenue-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='daily-revenue-comparison', className='line-chart', figure=revenue_figures.generate_daily_comparison(daily_revenue_analyzed, today))])
        ]),

        html.Div([
            html.Div([dcc.Graph(id='daily-revenue-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='weekly-revenue-chart', className='line-chart')]),
        ]),
    ],className='basic-grid'),

    html.Div([
        html.H3('Supplier'),
        html.P(f"Latest datum: {supplier_date}"),
        html.P('Select a supplier:'),
        dcc.Dropdown(
            id='supplier-dropdown',
            options=[{'label': supplier, 'value': supplier} for supplier in suppliers],
            value=suppliers[1],
            className='drop-down',
        ),
    ], className='drop-down-grid'),

    html.Div([
           html.Div([
            html.H5(f"All Suppliers Daily Count({latest_date_supplier}) :"),
            html.H2(f"{latest_data_sum:,}"),
            html.H3(f"{supplier_daily_dif:,}",  style={'color': sup_daily_dif_color})
        ],className='bfn-grid'),

        html.Div([
            html.H5('All Suppliers Weekly Count:'),
            html.H2(f"{recent_supplier_week_sum:,}"),
            html.H3(f"{weekly_supplier_difference:,}",  style={'color': supplier_weekly_color})
        ],className='bfn-grid'),

        html.Div([
            html.H5(f"Daily Count ({latest_date_supplier}) :"),
            html.H2(id='daily_supplier_count'),
            html.H3(id='bfn_supplier_daily_delta')
        ],className='bfn-grid'),

        html.Div([
            html.H5(f"Weekly Count:"),
            html.H2(id='weekly_supplier_count'),
            html.H3(id='bfn_supplier_weekly_delta')
        ],className='bfn-grid'),
    ], className='bfn-basic-grid'),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='weekly-supplier-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='daily-supplier-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='monthly-supplier-chart', className='line-chart')]),
        ]),
    ],className='basic-grid'),

    html.Div([
        html.H3('UTM'),
        html.P(f"Latest datum: {utm_date}"),
        html.P('Select a supplier:'),
        dcc.Dropdown(
            id='utm-supplier-dropdown',
            options=[{'label': supplier, 'value': supplier} for supplier in utm_suppliers],
            value=utm_suppliers[0],
            className='drop-down'
        ),
        html.P('Select an ad id:'),
      dcc.Dropdown(
          id='utm-ad-dropdown',
          options=[{'label': str(ad_id), 'value': ad_id} for ad_id in utm_ads],
          value=utm_ads[0],
          className='drop-down'
      ),
    ], className='drop-down-grid'),

    html.Div([
           html.Div([
            html.H5(f"Top ad for week ending ({utm_date})"),
            html.H2(f"{utm_winner}"),
            html.H3('')
        ],className='bfn-grid'),

        html.Div([
            html.H5(f"Bottom ad for week ending ({utm_date})"),
            html.H2(f"{utm_loser}"),
            html.H3('')
        ],className='bfn-grid'),
    ], className='bfn-basic-grid'),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='daily-utm-supplier-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='daily-utm-ad-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='weekly-utm-supplier-chart', className='line-chart')]),
        ]),

        html.Div([
            html.Div([dcc.Graph(id='weekly-utm-ad-chart', className='line-chart')]),
        ]),
    ],className='basic-grid'),

    html.Footer(children=[html.P('Copyright © 2023 - Candid Maven',  style={'textAlign': 'center'}),])
])

@application.callback(
    Output('bfn_weekly', 'children'),
    Output('bfn_weekly_difference', 'children'),
    Output('bfn_daily_difference', 'children'),
    Output('daily_revenue_bfn', 'children'),
    Output('daily-revenue-chart', 'figure'),
    Output('weekly-revenue-chart', 'figure'),
    Output('monthly-revenue-chart', 'figure'),
    Output('daily-supplier-chart', 'figure'),
    Output('weekly-supplier-chart', 'figure'),
    Output('monthly-supplier-chart', 'figure'),
    Output('daily_supplier_count', 'children'),
    Output('weekly_supplier_count', 'children'),
    Output('bfn_supplier_weekly_delta', 'children'),
    Output('bfn_supplier_daily_delta', 'children'),
    Output('daily-utm-supplier-chart', 'figure'),
    Output('daily-utm-ad-chart', 'figure'),
    Output('weekly-utm-supplier-chart', 'figure'),
    Output('weekly-utm-ad-chart', 'figure'),
    Input('company-dropdown', 'value'),
    Input('supplier-dropdown', 'value'),
    Input('utm-supplier-dropdown', 'value'),
    Input('utm-ad-dropdown', 'value')
)
def update_charts(selected_company, selected_supplier, selected_utm_supplier, selected_utm_ad ):
    
     # Revenue BFNs - Daily
    daily_delta = (daily_revenue_analyzed.loc[selected_company][-1] - daily_revenue_analyzed.loc[selected_company][-2] if selected_company in daily_revenue_analyzed.index else False
    )

    daily_revenue_bfn = (f"${'{:,.2f}'.format(daily_revenue_analyzed.loc[selected_company][-1])}") if selected_company in daily_revenue_analyzed.index else 'No data'
    
    bfn_daily_difference = html.H3(
        f"${'{:,.2f}'.format(daily_delta)}",
        style={'color': 'green' if daily_delta > 0 else 'red'} if daily_delta else {'color': 'black'}
    )  

    # Revenue BFNs - Weekly
    weekly_delta = (weekly_revenue_analyzed.loc[selected_company, 'recent_weekly_average'] - weekly_revenue_analyzed.loc[selected_company, 'previous_weekly_average']
    if selected_company in weekly_revenue_analyzed.index
    else False    
    )

    bfn_weekly = f"${'{:,.2f}'.format(weekly_revenue_analyzed.loc[selected_company, 'last_week_revenue'])}" if selected_company in weekly_revenue_analyzed.index else 'No data'

    bfn_weekly_difference = html.H3(
        f"${'{:,.2f}'.format(weekly_delta)}",
        style={'color': 'green' if weekly_delta > 0 else 'red'} if weekly_delta else {'color': 'black'}
    )  

    # Supplier BFNs - Weekly
    supplier_weekly_delta = (weekly_supplier_comparison["First Week"].loc[selected_supplier] - weekly_supplier_comparison["Second Week"].loc[selected_supplier]
    )

    bfn_supplier_weekly_delta = html.H3(
         f"{'{:,}'.format(supplier_weekly_delta)}",
        style={'color': 'green' if supplier_weekly_delta > 0 else 'red'} if supplier_weekly_delta else {'color': 'black'}
    )  

    #Suppliers BFNs - Daily
    daily_supplier_count = '{:,}'.format(daily_supplier_volume.loc[(daily_supplier_volume['Date'] == sorted(daily_supplier_volume['Date'].unique(), reverse=True)[1]) & (daily_supplier_volume['Supplier'].str.lower() == selected_supplier.lower()), 'Count'].values[0]) if selected_supplier.lower() in daily_supplier_volume['Supplier'].str.lower().values else "No Data"

    supplier_daily_delta = (daily_supplier_volume.loc[(daily_supplier_volume['Date'] == sorted(daily_supplier_volume['Date'].unique(), reverse=True)[1]) & (daily_supplier_volume['Supplier'].str.lower() == selected_supplier.lower()), 'Count'].values[0] - daily_supplier_volume.loc[(daily_supplier_volume['Date'] == sorted(daily_supplier_volume['Date'].unique(), reverse=True)[2]) & (daily_supplier_volume['Supplier'].str.lower() == selected_supplier.lower()), 'Count'].values[0] if selected_supplier.lower() in daily_supplier_volume['Supplier'].str.lower().values else False
    )

    bfn_supplier_daily_delta = html.H3(f"{'{:,}'.format(supplier_daily_delta)}",
        style={'color': 'green' if supplier_daily_delta > 0 else 'red'} if supplier_daily_delta else {'color': 'black'}
    )

    # Supplier BFN - Weekly
    weekly_supplier_count = '{:,}'.format(weekly_supplier_comparison["Second Week"].loc[selected_supplier])

    # Revenue
    daily_revenue = (
        revenue_figures.generate_daily_chart(selected_company, daily_revenue_analyzed, today)
        if selected_company in daily_revenue_analyzed.index
        else revenue_figures.handle_empty()
    )
    weekly_revenue = (
        revenue_figures.generate_weekly_chart(selected_company, weekly_revenue_analyzed, today)
        if selected_company in weekly_revenue_analyzed.index
        else revenue_figures.handle_empty()
    )
    monthly_revenue = (
        revenue_figures.generate_cumulative_chart(
            selected_company, last_month_revenue_cumulative, this_month_revenue_cumulative, today
        )
        if selected_company in last_month_revenue_cumulative.index
        and selected_company in this_month_revenue_cumulative.index
        else revenue_figures.handle_empty()
    )

    # Supplier
    daily_supplier = supplier_figures.generate_daily_supplier_chart(selected_supplier, daily_supplier_volume)

    weekly_supplier = supplier_figures.generate_supplier_comparison_chart(weekly_supplier_comparison)

    monthly_supplier = supplier_figures.generate_weekly_volume_chart(selected_supplier, monthly_supplier_volume)

    # UTM
    daily_utm_supplier = utm_figures.generate_daily_utm_supplier_chart(selected_utm_supplier, daily_utm_data)
    daily_utm_ad = utm_figures.generate_daily_utm_ad_chart(selected_utm_ad, daily_utm_data)
    weekly_utm_supplier = utm_figures.generate_weekly_utm_supplier_chart(selected_utm_supplier, weekly_utm_data)
    weekly_utm_ad = utm_figures.generate_weekly_utm_ad_chart(selected_utm_ad, weekly_utm_data)
   
    return bfn_weekly, bfn_weekly_difference, bfn_daily_difference, daily_revenue_bfn, daily_revenue, weekly_revenue, monthly_revenue, daily_supplier, weekly_supplier, monthly_supplier,daily_supplier_count, weekly_supplier_count,bfn_supplier_weekly_delta,bfn_supplier_daily_delta, daily_utm_supplier, daily_utm_ad, weekly_utm_supplier, weekly_utm_ad

# Generate the HTML content for the index.html file
index_html = application.index_string

# Save the index.html file
# with open("index.html", "w") as file:
#     file.write(index_html)

# if __name__ == '__main__':
#     if not DEPLOYED_STATUS:
#         # Automate finding default port when in development environment
#         port = 80
#         while True:
#             try:
#                 application.run_server(debug=True, port=port)
#                 break
#             except OSError:
#                 port += 1
#     else: # Run server deployed
#         # application.run_server(debug=True)
#         with open("index.html", "w") as file:
#             file.write(index_html)

if __name__ == '__main__':
  # Automate finding default port when in development environment
  port = 3000
  while True:
      try:
          application.run_server(debug=True, port=port)
          break
      except:
          port += 1
