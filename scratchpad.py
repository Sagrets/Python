import dash
import dash_bootstrap_components as dbc
from dash import dcc,html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.H1('Financial Dashboard', className='Headings'),
                    sm=4
                )
            ],
            justify='start',
            align='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='y-axis-dropdown',
                        options=[{'label': i, 'value': i} for i in df.select_dtypes(include='number').columns],
                        value=df.select_dtypes(include='number').columns[0],
                    ),
                    sm=4,
                    className='Dropdown_Color_Styling'
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='x-axis-dropdown',
                        options=[{'label': i, 'value': i} for i in df.select_dtypes(include='number').columns],
                        value=df.select_dtypes(include='number').columns[1]
                    ),
                    sm=4,
                    className='Dropdown_Color_Styling'
                )
            ],
            align='center',
            justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='Correlation-ScatterPlot', figure={}),
                    sm=6
                ),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure = Total_loan_Amount,
                                    style={"height": "45vh"}
                                ),
                                sm=3    
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    figure=Avg_Loan_Amount,
                                    style={"height": "45vh"}
                                ),
                                sm=3
                            )
                        ],
                        className='g-0',
                        align='start'
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=Avg_Loan_Amount_Term,
                                    style={'height': '45vh'}
                                ),
                                sm=3
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    figure=Total_loans,
                                    style={'45vh'}
                                ),
                                sm=3
                            )
                        ],
                        className='g-0',
                        align='start'
                    ),
                    sm=6
                )
            ],
            align='start' 
        )    
    ],
    className='Main_Div'
)
