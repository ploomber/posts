import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample sales data
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
sales = np.random.normal(1000, 200, len(dates))
products = ["Product A", "Product B", "Product C", "Product D"]
product_sales = {p: np.random.normal(1000, 200, len(dates)) for p in products}

df = pd.DataFrame(
    {
        "Date": dates,
        "Total_Sales": sales,
        **{f"{p}_Sales": product_sales[p] for p in products},
    }
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Create layout
app.layout = html.Div(
    [
        html.H1("Sales Dashboard", style={"textAlign": "center"}),
        html.Div(
            [
                # Total Sales Time Series
                html.Div(
                    [
                        html.H3("Total Sales Over Time"),
                        dcc.Graph(
                            figure=px.line(
                                df, x="Date", y="Total_Sales", title="Daily Total Sales"
                            )
                        ),
                    ],
                    style={"width": "100%", "marginBottom": "20px"},
                ),
                # Product Sales Comparison
                html.Div(
                    [
                        html.H3("Product Sales Comparison"),
                        dcc.Graph(
                            figure=go.Figure(
                                [
                                    go.Bar(name=p, x=df["Date"], y=df[f"{p}_Sales"])
                                    for p in products
                                ]
                            ).update_layout(
                                barmode="stack", title="Daily Product Sales"
                            )
                        ),
                    ],
                    style={"width": "100%", "marginBottom": "20px"},
                ),
                # Summary Statistics
                html.Div(
                    [
                        html.H3("Summary Statistics"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4("Total Revenue"),
                                        html.H2(f"${df['Total_Sales'].sum():,.2f}"),
                                    ],
                                    style={
                                        "width": "33%",
                                        "display": "inline-block",
                                        "textAlign": "center",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H4("Average Daily Sales"),
                                        html.H2(f"${df['Total_Sales'].mean():,.2f}"),
                                    ],
                                    style={
                                        "width": "33%",
                                        "display": "inline-block",
                                        "textAlign": "center",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.H4("Best Selling Product"),
                                        html.H2(
                                            max(
                                                products,
                                                key=lambda p: df[f"{p}_Sales"].sum(),
                                            )
                                        ),
                                    ],
                                    style={
                                        "width": "33%",
                                        "display": "inline-block",
                                        "textAlign": "center",
                                    },
                                ),
                            ]
                        ),
                    ],
                    style={"width": "100%", "marginBottom": "20px"},
                ),
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
