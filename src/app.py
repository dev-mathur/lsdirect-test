import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your dataframes
products = pd.read_csv("products.csv")
stores = pd.read_csv("stores.csv")
transactions = pd.read_csv("transactions.csv")

# Prepare the dropdown options
store_options = [{'label': i, 'value': i} for i in stores['StoreID'].unique()]

# Initialize the Dash app
app = dash.Dash(__name__)

#Needed for deployment
server = app.server

# Define the layout of the Dash app
app.layout = html.Div(children=[
    html.H1(children='Interactive Store Data'),

    html.Div(children='''Visualizing Sales and Revenue Data.'''),

    dcc.Dropdown(
        id='store-selector',
        options=store_options,
        value=store_options[0]['value'],  # default value
        clearable=False
    ),

    dcc.Graph(id='sales-trends'),
    dcc.Graph(id='revenue-distribution'),
    dcc.Graph(id='revenue-by-day')
])

# Callback for updating the sales-trends graph
@app.callback(
    Output('sales-trends', 'figure'),
    Input('store-selector', 'value')
)
def update_sales_trends(selected_store):
    # Merge transactions with products on ProductID or the appropriate key
    merged_transactions = pd.merge(transactions, products, on='ProductID', how='left')
    filtered_transactions = merged_transactions[merged_transactions['StoreID'] == selected_store]
    filtered_transactions['PurchaseDate'] = pd.to_datetime(filtered_transactions['PurchaseDate'])
    transactions_per_day = filtered_transactions.groupby('PurchaseDate').size().reset_index(name='Transactions')
    fig = px.line(transactions_per_day, x='PurchaseDate', y='Transactions', title=f'Daily Transactions for Store {selected_store}')
    return fig

# Callback for updating the revenue-distribution graph
@app.callback(
    Output('revenue-distribution', 'figure'),
    Input('store-selector', 'value')
)
def update_revenue_distribution(selected_store):
    # Merge transactions with products on ProductID or the appropriate key
    merged_transactions = pd.merge(transactions, products, on='ProductID', how='left')
    filtered_transactions = merged_transactions[merged_transactions['StoreID'] == selected_store]
    filtered_transactions = filtered_transactions.drop('Price_y', axis=1)
    filtered_transactions = filtered_transactions.rename(columns={'Price_x': 'Price'})
    filtered_transactions['Price'] = filtered_transactions['Price'].replace('[\$,]', '', regex=True).astype(float)
    revenue_per_category = filtered_transactions.groupby('ProductCategory')['Price'].sum().reset_index()
    fig = px.pie(revenue_per_category, values='Price', names='ProductCategory', title=f'Revenue Distribution By Product Categories for Store {selected_store}')
    return fig

# Callback for updating the revenue-by-day graph
@app.callback(
    Output('revenue-by-day', 'figure'),
    Input('store-selector', 'value')
)
def update_revenue_by_day(selected_store):
    # Merge transactions with products on ProductID or the appropriate key
    merged_transactions = pd.merge(transactions, products, on='ProductID', how='left')
    filtered_transactions = merged_transactions[merged_transactions['StoreID'] == selected_store]
    filtered_transactions = filtered_transactions.drop('Price_y', axis=1)
    filtered_transactions = filtered_transactions.rename(columns={'Price_x': 'Price'})
    filtered_transactions['Price'] = filtered_transactions['Price'].replace('[\$,]', '', regex=True).astype(float)
    filtered_transactions['PurchaseDate'] = pd.to_datetime(filtered_transactions['PurchaseDate'])
    filtered_transactions['DayOfWeek'] = filtered_transactions['PurchaseDate'].dt.day_name()
    revenue_per_day = filtered_transactions.groupby(['DayOfWeek', 'ProductCategory'])['Price'].sum().reset_index()
    pivot_data = revenue_per_day.pivot(index='DayOfWeek', columns='ProductCategory', values='Price').fillna(0)
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex(days_order)
    fig = px.bar(pivot_data, title=f'Revenue by Day of the Week for Store {selected_store}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)