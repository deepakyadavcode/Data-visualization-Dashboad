import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("data.csv")

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("📊 Interactive Data Visualization Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Category:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],
            value=df['Category'].unique()[0]
        )
    ], style={'width': '40%', 'margin': 'auto'}),

    html.Br(),

    dcc.Graph(id='plotly-graph'),

    html.Img(id='matplotlib-plot', style={'display': 'block', 'margin': 'auto', 'width': '80%'})
])

# Callback for Plotly Graph
@app.callback(
    Output('plotly-graph', 'figure'),
    Input('category-dropdown', 'value')
)
def update_plotly_graph(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    fig = px.line(filtered_df, x='Date', y='Sales', title=f"Sales Trend for Category {selected_category}")
    fig.update_layout(template='plotly_dark')
    return fig

# Callback for Matplotlib Image
@app.callback(
    Output('matplotlib-plot', 'src'),
    Input('category-dropdown', 'value')
)
def update_matplotlib_plot(selected_category):
    filtered_df = df[df['Category'] == selected_category]

    # Create a Matplotlib plot
    plt.figure(figsize=(6,4))
    plt.bar(filtered_df['Date'], filtered_df['Profit'], color='teal')
    plt.title(f'Profit Bar Chart for Category {selected_category}')
    plt.xlabel('Date')
    plt.ylabel('Profit')
    plt.tight_layout()

    # Save plot to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    encoded = base64.b64encode(image_png).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
