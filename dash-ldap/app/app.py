import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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

# Add Tailwind CSS
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body class="bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen p-8">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Create layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Sales Dashboard",
                    className="text-4xl font-light text-center text-slate-800 mb-8",
                ),
                html.A(
                    html.Button(
                        "Logout",
                        className="absolute top-4 right-4 px-4 py-2 bg-slate-600 text-white rounded-lg hover:bg-slate-700 transition-colors duration-200",
                    ),
                    href="/logout",
                    className="no-underline",
                ),
            ],
            className="relative",
        ),
        html.Div(
            [
                # Total Sales Time Series
                html.Div(
                    [
                        html.H3(
                            "Total Sales Over Time",
                            className="text-xl font-medium text-slate-700 mb-4",
                        ),
                        dcc.Graph(
                            figure=px.line(
                                df, x="Date", y="Total_Sales", title="Daily Total Sales"
                            )
                        ),
                    ],
                    className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 mb-8",
                ),
                # Product Sales Comparison
                html.Div(
                    [
                        html.H3(
                            "Product Sales Comparison",
                            className="text-xl font-medium text-slate-700 mb-4",
                        ),
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
                    className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6 mb-8",
                ),
                # Summary Statistics
                html.Div(
                    [
                        html.H3(
                            "Summary Statistics",
                            className="text-xl font-medium text-slate-700 mb-6",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            "Total Revenue",
                                            className="text-sm font-medium text-slate-600 mb-2",
                                        ),
                                        html.H2(
                                            f"${df['Total_Sales'].sum():,.2f}",
                                            className="text-2xl font-semibold text-slate-800",
                                        ),
                                    ],
                                    className="w-1/3 text-center",
                                ),
                                html.Div(
                                    [
                                        html.H4(
                                            "Average Daily Sales",
                                            className="text-sm font-medium text-slate-600 mb-2",
                                        ),
                                        html.H2(
                                            f"${df['Total_Sales'].mean():,.2f}",
                                            className="text-2xl font-semibold text-slate-800",
                                        ),
                                    ],
                                    className="w-1/3 text-center",
                                ),
                                html.Div(
                                    [
                                        html.H4(
                                            "Best Selling Product",
                                            className="text-sm font-medium text-slate-600 mb-2",
                                        ),
                                        html.H2(
                                            max(
                                                products,
                                                key=lambda p: df[f"{p}_Sales"].sum(),
                                            ),
                                            className="text-2xl font-semibold text-slate-800",
                                        ),
                                    ],
                                    className="w-1/3 text-center",
                                ),
                            ],
                            className="flex justify-between",
                        ),
                    ],
                    className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg p-6",
                ),
            ],
            className="max-w-7xl mx-auto",
        ),
    ],
    className="container mx-auto",
)

if __name__ == "__main__":
    app.run_server(debug=False, port=8501)
