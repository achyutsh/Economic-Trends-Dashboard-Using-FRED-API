# Import necessary libraries
# Dash: for creating the web dashboard
# Plotly: for creating interactive plots
# Pandas: for data manipulation and analysis
# Requests: for making HTTP requests to APIs
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import requests

# API key
API_KEY = "a78e5c6ae5b633ab525a8db1963f8009"


# Define a function to fetch data from the FRED API
def fetch_data(api_key):
    # Endpoints for various economic indicators
    urls = {
        'unemployment': f'https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={api_key}&file_type=json',
        'gdp': f'https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={api_key}&file_type=json',
        'cpi': f'https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={api_key}&file_type=json',
        'interest_rate': f'https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={api_key}&file_type=json'
    }
    # Fetch data and store it in a dictionary
    # Ensure error handling for failed requests
    data = {}
    for key, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            data[key] = response.json()
        else:
            print(f"Failed to fetch {key}: {response.status_code}")
    return data


# Define functions to process the API data

# Convert API response JSON into pandas DataFrames

def load_data_to_df(data):
    dfs = {key: pd.DataFrame(value['observations']) for key, value in data.items()}

    # Standardize column formats (e.g., numeric values, datetime index)

    for df in dfs.values():
        # Convert 'value' to numeric

        df['value'] = pd.to_numeric(df['value'], errors='coerce')

        # Convert 'date' to datetime

        df['date'] = pd.to_datetime(df['date'])

    return dfs


# Merge multiple DataFrames into a single DataFrame

def merge_data(dfs):
    df_combined = pd.merge(dfs['unemployment'][['date', 'value']], dfs['gdp'][['date', 'value']], on='date',
                           how='outer', suffixes=('_unemployment', '_gdp'))

    df_combined = pd.merge(df_combined, dfs['cpi'][['date', 'value']], on='date', how='outer')

    df_combined = pd.merge(df_combined, dfs['interest_rate'][['date', 'value']], on='date', how='outer',
                           suffixes=('_cpi', '_interest_rate'))

    # Rename columns for clarity and fill missing values

    df_combined.rename(columns={'value': 'value_cpi', 'value_interest_rate': 'value_interest_rate'}, inplace=True)

    df_combined.sort_values('date', inplace=True)

    # Forward-fill to handle missing data

    df_combined.ffill(inplace=True)

    return df_combined


# Define a function to calculate Key Performance Indicators (KPIs)

def calculate_kpis(df):
    """

    Calculate summary statistics to derive key performance indicators (KPIs) from the combined dataset.

    Args:

    df (pd.DataFrame): A pandas DataFrame containing economic indicators with columns for unemployment rate, GDP, CPI,

                       and interest rate.

    Returns:

    dict: A dictionary containing the calculated KPIs.

    """

    return {

        # Calculate the average unemployment rate and round it to two decimal places

        'Average Unemployment Rate': round(df['value_unemployment'].mean(), 2),

        # Find the maximum GDP value in the dataset and round it to two decimal places

        'Max GDP': round(df['value_gdp'].max(), 2),

        # Determine the minimum value of CPI (Consumer Price Index) and round it to two decimal places

        'Min CPI': round(df['value_cpi'].min(), 2),

        # Compute the median interest rate from the dataset and round it to two decimal places

        'Median Interest Rate': round(df['value_interest_rate'].median(), 2)

    }


# Fetch, load, and merge data

data = fetch_data(API_KEY)

dfs = load_data_to_df(data)

df_combined = merge_data(dfs)

kpis = calculate_kpis(df_combined)

df_combined.head()

# Create the Dash app

app = dash.Dash(__name__)

# Define the app layout

app.layout = html.Div([  # Main container for the app

    html.H1("Economic Data Dashboard", style={'textAlign': 'center'}),  # Dashboard title

    # Display Key Performance Indicators (KPIs)

    html.Div([

        html.H3("Key Performance Indicators:"),  # Section header

        html.P(f"Average Unemployment Rate: {kpis['Average Unemployment Rate']}%"),  # Display average unemployment

        html.P(f"Maximum GDP: {kpis['Max GDP']} (in billions)"),  # Display max GDP

        html.P(f"Minimum CPI: {kpis['Min CPI']}"),  # Display min CPI

        html.P(f"Median Interest Rate: {kpis['Median Interest Rate']}%"),  # Display median interest rate

    ], style={'margin': '20px'}),  # Styling for KPI section

    # Tabs for visualizing data

    dcc.Tabs([

        dcc.Tab(label='Unemployment Rate', children=[  # Tab for unemployment data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_unemployment',

                                     title="Unemployment Rate Over Time"))  # Line chart for unemployment

        ]),

        dcc.Tab(label='GDP', children=[  # Tab for GDP data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_gdp', title="GDP Over Time"))  # Line chart for GDP

        ]),

        dcc.Tab(label='CPI', children=[  # Tab for CPI data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_cpi', title="CPI Over Time"))  # Line chart for CPI

        ]),

        dcc.Tab(label='Interest Rate', children=[  # Tab for interest rate data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_interest_rate',

                                     title="Interest Rate Over Time"))  # Line chart for interest rates

        ]),

    ])

])# Import necessary libraries
# Dash: for creating the web dashboard
# Plotly: for creating interactive plots
# Pandas: for data manipulation and analysis
# Requests: for making HTTP requests to APIs
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import requests

# API key
API_KEY = "a78e5c6ae5b633ab525a8db1963f8009"


# Define a function to fetch data from the FRED API
def fetch_data(api_key):
    # Endpoints for various economic indicators
    urls = {
        'unemployment': f'https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={api_key}&file_type=json',
        'gdp': f'https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={api_key}&file_type=json',
        'cpi': f'https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={api_key}&file_type=json',
        'interest_rate': f'https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={api_key}&file_type=json'
    }
    # Fetch data and store it in a dictionary
    # Ensure error handling for failed requests
    data = {}
    for key, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            data[key] = response.json()
        else:
            print(f"Failed to fetch {key}: {response.status_code}")
    return data


# Define functions to process the API data

# Convert API response JSON into pandas DataFrames

def load_data_to_df(data):
    dfs = {key: pd.DataFrame(value['observations']) for key, value in data.items()}

    # Standardize column formats (e.g., numeric values, datetime index)

    for df in dfs.values():
        # Convert 'value' to numeric

        df['value'] = pd.to_numeric(df['value'], errors='coerce')

        # Convert 'date' to datetime

        df['date'] = pd.to_datetime(df['date'])

    return dfs


# Merge multiple DataFrames into a single DataFrame

def merge_data(dfs):
    df_combined = pd.merge(dfs['unemployment'][['date', 'value']], dfs['gdp'][['date', 'value']], on='date',
                           how='outer', suffixes=('_unemployment', '_gdp'))

    df_combined = pd.merge(df_combined, dfs['cpi'][['date', 'value']], on='date', how='outer')

    df_combined = pd.merge(df_combined, dfs['interest_rate'][['date', 'value']], on='date', how='outer',
                           suffixes=('_cpi', '_interest_rate'))

    # Rename columns for clarity and fill missing values

    df_combined.rename(columns={'value': 'value_cpi', 'value_interest_rate': 'value_interest_rate'}, inplace=True)

    df_combined.sort_values('date', inplace=True)

    # Forward-fill to handle missing data

    df_combined.ffill(inplace=True)

    return df_combined


# Define a function to calculate Key Performance Indicators (KPIs)

def calculate_kpis(df):
    """

    Calculate summary statistics to derive key performance indicators (KPIs) from the combined dataset.

    Args:

    df (pd.DataFrame): A pandas DataFrame containing economic indicators with columns for unemployment rate, GDP, CPI,

                       and interest rate.

    Returns:

    dict: A dictionary containing the calculated KPIs.

    """

    return {

        # Calculate the average unemployment rate and round it to two decimal places

        'Average Unemployment Rate': round(df['value_unemployment'].mean(), 2),

        # Find the maximum GDP value in the dataset and round it to two decimal places

        'Max GDP': round(df['value_gdp'].max(), 2),

        # Determine the minimum value of CPI (Consumer Price Index) and round it to two decimal places

        'Min CPI': round(df['value_cpi'].min(), 2),

        # Compute the median interest rate from the dataset and round it to two decimal places

        'Median Interest Rate': round(df['value_interest_rate'].median(), 2)

    }


# Fetch, load, and merge data

data = fetch_data(API_KEY)

dfs = load_data_to_df(data)

df_combined = merge_data(dfs)

kpis = calculate_kpis(df_combined)

df_combined.head()

# Create the Dash app

app = dash.Dash(__name__)

# Define the app layout

app.layout = html.Div([  # Main container for the app

    html.H1("Economic Data Dashboard", style={'textAlign': 'center'}),  # Dashboard title

    # Display Key Performance Indicators (KPIs)

    html.Div([

        html.H3("Key Performance Indicators:"),  # Section header

        html.P(f"Average Unemployment Rate: {kpis['Average Unemployment Rate']}%"),  # Display average unemployment

        html.P(f"Maximum GDP: {kpis['Max GDP']} (in billions)"),  # Display max GDP

        html.P(f"Minimum CPI: {kpis['Min CPI']}"),  # Display min CPI

        html.P(f"Median Interest Rate: {kpis['Median Interest Rate']}%"),  # Display median interest rate

    ], style={'margin': '20px'}),  # Styling for KPI section

    # Tabs for visualizing data

    dcc.Tabs([

        dcc.Tab(label='Unemployment Rate', children=[  # Tab for unemployment data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_unemployment',

                                     title="Unemployment Rate Over Time"))  # Line chart for unemployment

        ]),

        dcc.Tab(label='GDP', children=[  # Tab for GDP data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_gdp', title="GDP Over Time"))  # Line chart for GDP

        ]),

        dcc.Tab(label='CPI', children=[  # Tab for CPI data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_cpi', title="CPI Over Time"))  # Line chart for CPI

        ]),

        dcc.Tab(label='Interest Rate', children=[  # Tab for interest rate data

            dcc.Graph(figure=px.line(df_combined, x='date', y='value_interest_rate',

                                     title="Interest Rate Over Time"))  # Line chart for interest rates

        ]),

    ])

])

# Run the app

if __name__ == '__main__':
    app.run_server(debug=True, port=8081) #update the port number to any immediate upcoming number to run the code

# Run the app

if __name__ == '__main__':
    app.run_server(debug=True, port=8081) #update the port number to any immediate upcoming number to run the code