import pandas as pd
import sqlalchemy as sql
from cryptography.fernet import Fernet
import os
from scipy.stats import spearmanr
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc



def load_env(env_file, key):
    with open(key,'rb') as filekey:
        key = filekey.read()

    with open(env_file, 'rb') as environment:
        encrypted_data = environment.read()

    fernet = Fernet(key)

    decrypted_data = fernet.decrypt(encrypted_data)

    env_vars = {}

    for line in decrypted_data.splitlines():
        key, value = line.decode().split('=', 1)
        env_vars[key] = value
    
    os.environ.update(env_vars)

    return env_vars

env_vars = load_env('.env', 'INSERT THE FILEPATH TO YOUR ENCRYPTION KEY HERE.')
engine = sql.create_engine(f'mysql+pymysql://{os.getenv('DB_User')}:{os.getenv('DB_Password')}@{os.getenv('DB_Host')}/financialdb')
df = pd.read_sql_query('SELECT * FROM onbook_loans', engine)

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            'name': 'viewport',
            'content': 'width=device-width, height=device-height, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover'
        }    
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

Total_Loan_Amount = go.Figure(go.Indicator(
    mode = 'gauge+number',
    value = pd.read_sql_query('SELECT sum(LoanAmount) FROM onbook_loans', engine).iloc[0,0],
    title = {'text': 'Total Loan Amount', 'font': {'size': 24, 'color': '#51A1FF'}},
    gauge = {
        'axis': {'range': [40000, 120000], 'dtick': 10000, 'tick0': 40000, 'tickfont': {'color': '#51A1FF'}},
        'bar': {'color': '#51A1FF'},
        'bgcolor': 'gray',
        'bordercolor': 'gray'
    },
    number={'font': {'color': '#51A1FF'}}
))
Total_Loan_Amount.update_layout(paper_bgcolor = 'black')

Avg_Loan_Amount = go.Figure(go.Indicator(
    mode = 'gauge+number',
    value = pd.read_sql_query('SELECT avg(LoanAmount) FROM onbook_loans', engine).iloc[0,0] * 1000,
    title = {'text': 'Average Loan Amount', 'font': {'size': 24, 'color': '#51A1FF'}},
    gauge = {
        'axis': {'range': [0, 300000], 'dtick': 40000, 'tick0': 30000, 'tickfont': {'color': '#51A1FF'}},
        'bar': {'color': '#51A1FF'},
        'bgcolor': 'gray',
        'bordercolor': 'gray'
    },
    number={'font': {'color': '#51A1FF'}}
))
Avg_Loan_Amount.update_layout(paper_bgcolor = 'black')

Avg_Loan_Amount_Term = go.Figure(go.Indicator(
    mode = 'gauge+number',
    value = pd.read_sql_query('SELECT avg(Loan_Amount_Term) FROM onbook_loans', engine).iloc[0,0],
    title = {'text': 'Average Loan Amount<br>Term', 'font': {'size': 24, 'color': '#51A1FF'}},
    gauge = {
        'axis': {'range': [0, 400], 'dtick': 50, 'tick0': 100, 'tickfont': {'color': '#51A1FF'}},
        'bar': {'color': '#51A1FF'},
        'bgcolor': 'gray',
        'bordercolor': 'gray'
    },
    number={'font': {'color': '#51A1FF'}}
))
Avg_Loan_Amount_Term.update_layout(paper_bgcolor = 'black')

Total_Loans = go.Figure(go.Indicator(
    mode = 'gauge+number',
    value = pd.read_sql_query('SELECT COUNT(DISTINCT Loan_ID) FROM onbook_loans', engine).iloc[0,0],
    title = {'text': 'Total Loans', 'font': {'size': 24, 'color': '#51A1FF'}},
    gauge = {
        'axis': {'range': [100, 600], 'dtick': 60, 'tick0': 200, 'tickfont': {'color': '#51A1FF'}},
        'bar': {'color': '#51A1FF'},
        'bgcolor': 'gray',
        'bordercolor': 'gray'
        },
        number={'font': {'color': '#51A1FF'}}
))
Total_Loans.update_layout(paper_bgcolor = 'black')

education_percent = go.Figure(go.Indicator(
  mode = 'number+gauge',
  gauge = {'shape': 'bullet', 'bar': {'color': '#51A1FF'}},
  number={'font': {'color': '#51A1FF'}},
  value = pd.read_sql_query('SELECT TRUNCATE((COUNT(CASE WHEN Education = "Graduate" THEN 1 END) * 1.0 / COUNT(*)) * 100, 2) AS graduate_ratio FROM onbook_loans;', engine).iloc[0,0]
))
education_percent.update_layout(
    title={
        'text': 'Percentage of applicants with a College Degree',
        'y': 0.9,
        'x': 0.5,
        'yanchor': 'top',
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#51A1FF'}
    },
    paper_bgcolor='black'
)

self_employed_percent = go.Figure(go.Indicator(
    mode = 'number+gauge',
    gauge = {'shape': 'bullet', 'bar': {'color': '#51A1FF'}},
    number = {'font': {'color': '#51A1FF'}},
    value = pd.read_sql_query('SELECT TRUNCATE((COUNT(CASE WHEN Self_Employed = "Yes" THEN 1 END) * 1.0 / COUNT(*)) * 100, 2) AS self_employed_ratio FROM onbook_loans;', engine).iloc[0,0]
))
self_employed_percent.update_layout(
    title = {
        'text': 'Percentage of applicants who are self employed',
        'y': 0.9,
        'x': 0.5,
        'yanchor': 'top',
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#51A1FF'}
    },
    paper_bgcolor='black'
)

approved_denied_loans = go.Figure(data=[go.Pie(
    labels=['Approved', 'Denied'],
    values=[
        pd.read_sql_query("select count(Loan_Status) from onbook_loans where Loan_Status = 'Y'", engine).iloc[0,0],
        pd.read_sql_query("select count(Loan_Status) from onbook_loans where Loan_Status = 'N'", engine).iloc[0,0]
    ]
)])
approved_denied_loans.update_layout(
    title = {
        'text': 'Approved VS Denied<br>Loans',
        'y': 0.8,
        'x': 0.5,
        'yanchor': 'top',
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#51A1FF'}
    },
    paper_bgcolor='black',
    legend=dict(
        x=1,
        xanchor='left',
        y=0,
        yanchor='bottom'
    )
)
approved_denied_loans.update_traces(marker=dict(colors=['#51A1FF', '#FFFFFF']))

good_bad_credit_loans = go.Figure(data=[go.Pie(
    labels=['Good Credit', 'Bad Credit'],
    values=[
        pd.read_sql_query("select count(Credit_History) from onbook_loans where Credit_History = 1", engine).iloc[0,0],
        pd.read_sql_query("select count(Credit_History) from onbook_loans where Credit_History = 0", engine).iloc[0,0]
    ]
)])
good_bad_credit_loans.update_layout(
    title = {
        'text': 'Good VS Bad Loans',
        'y': 0.9,
        'x': 0.5,
        'yanchor': 'top',
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#51A1FF'}
    },
    paper_bgcolor='black',
    legend=dict(
        x=1,
        xanchor='left',
        y=0,
        yanchor='bottom'
    )
)
good_bad_credit_loans.update_traces(marker=dict(colors=['#51A1FF', '#FFFFFF']))

Max_Loan_Term = go.Figure(go.Indicator(
    mode = 'gauge+number',
    value = pd.read_sql_query('select max(loan_amount_term) from onbook_loans', engine).iloc[0,0],
    title = {'text': 'Max Loan Term', 'font': {'size': 24, 'color': '#51A1FF'}},
    gauge = {
        'axis': {'range': [0, 600], 'dtick': 80, 'tick0': 100, 'tickfont': {'color': '#51A1FF'}},
        'bar': {'color': '#51A1FF'},
        'bgcolor': 'gray',
        'bordercolor': 'gray'
    },
    number={'font': {'color': '#51A1FF'}}
))
Max_Loan_Term.update_layout(paper_bgcolor = 'black')

Min_Loan_Term = go.Figure(go.Indicator(
    mode = 'gauge+number',
    value = pd.read_sql_query('select min(loan_amount_term) from onbook_loans', engine).iloc[0,0],
    title = {'text': 'Minimum Loan Term', 'font': {'size': 24, 'color': '#51A1FF'}},
    gauge = {
        'axis': {'range': [0, 100], 'dtick': 20, 'tick0': 100, 'tickfont': {'color': '#51A1FF'}},
        'bar': {'color': '#51A1FF'},
        'bgcolor': 'gray',
        'bordercolor': 'gray'
    },
    number={'font': {'color': '#51A1FF'}}
))
Min_Loan_Term.update_layout(paper_bgcolor = 'black')

app.layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.H1('Financial Dashboard', className='Headings'),
                    sm=4,
                )
            ],
            justify='start',
            align='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='y-axis-dropdown',
                            options=[{'label': i, 'value': i} for i in df.select_dtypes(include='number').columns],
                            value=df.select_dtypes(include='number').columns[0],
                            className='Dropdowns'
                        )
                    ),
                    sm=2
                ),
                dbc.Col(
                    html.Div(
                        dcc.Dropdown(
                            id='x-axis-dropdown',
                            options=[{'label': i, 'value': i} for i in df.select_dtypes(include='number').columns],
                            value=df.select_dtypes(include='number').columns[1],
                            className='Dropdowns'
                        )
                    ),
                    sm=2
                )
            ],
            align='center',
            justify='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='Correlation-ScatterPlot', figure={}, className='containers scatter_height'),
                    sm=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=Total_Loan_Amount,
                                                className='graphs containers'
                                            ),
                                            sm=6
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=Avg_Loan_Amount,
                                                className='graphs containers'
                                            ),
                                            sm=6
                                        )
                                    ],
                                    className='g-1 pb-1',
                                    align='start'
                                )
                            ),
                            html.Div(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=Avg_Loan_Amount_Term,
                                                className='graphs containers'
                                            ),
                                            sm=6,
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=Total_Loans,
                                                className='graphs containers'
                                            ),
                                            sm=6,
                                        )
                                    ],
                                    className='g-1 pb-1',
                                    align='start'
                                )
                            )
                        ]
                    ),
                    sm=6
                )
            ],
            className='g-1',
            align='start'
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=education_percent,
                        className='containers slider_positioning'
                    ),
                    sm=6
                ),
                dbc.Col(
                    dcc.Graph(
                        figure=self_employed_percent,
                        className='containers slider_positioning'
                    ),
                    sm=6
                )
            ],
            className='g-1'
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='slider_dropdown',
                                    options=['ApplicantIncome', 'CoapplicantIncome', 'Total_Income'],
                                    value='ApplicantIncome',
                                    style={'zIndex': '1'},
                                    className='Dropdowns slider_dropdown'
                                )
                            ),
                            sm=2
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='dynamic_bar_graph_menu',
                                options=['Gender', 'Married', 'Property_Area'],
                                value='Gender',
                                style={'zIndex': '1'},
                                className='Dropdowns dynamic_bar_graph_menu'
                            ),
                            sm=2
                        )
                    ],
                    justify='around'
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id='dynamic_slider', figure={}, className='containers dynamic_slider', style={'zIndex': '0'}), sm=6),
                        dbc.Col(dcc.Graph(id='dynamic_bar_graph', figure={}, className='containers dynamic_bar_graph', style={'zIndex': '0'}), sm=6)
                    ],
                    className='g-1'
                )
            ],
            className='slider_div'
        ),
        html.Div(
            [
                dbc.Row(
                    [
                    dbc.Col(dcc.Graph(figure=approved_denied_loans, className='containers approval_pie_chart'), sm=3),
                    dbc.Col(dcc.Graph(figure=good_bad_credit_loans, className='containers credit_pie_chart'), sm=3)
                    ],
                    className='g-1'
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=Max_Loan_Term, className='containers term_graphs'), sm=6),
                dbc.Col(dcc.Graph(figure=Min_Loan_Term, className='containers term_graphs'), sm=6)
            ],
            className='g-1'
        )
    ],
    className='Main_Div'
)

@app.callback(
    Output(component_id='Correlation-ScatterPlot', component_property='figure'),
    [Input(component_id='y-axis-dropdown', component_property='value'),
     Input(component_id='x-axis-dropdown', component_property='value')]
)
def update_graph(y_axis, x_axis):
    fig = px.scatter(df, y=y_axis, x=x_axis)
    
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='#51A1FF'
    )
    
    return fig

@app.callback(
    Output(component_id='dynamic_slider', component_property='figure'),
    Input(component_id='slider_dropdown', component_property='value')
)
def update_slider(column):
    fig = go.Figure(go.Indicator(
        mode='number+gauge',
        gauge={'shape': 'bullet', 'bar': {'color': '#51A1FF'}},
        number={'suffix': 'k', 'font': {'color': '#51A1FF'}},
        value=pd.read_sql(f'SELECT TRUNCATE(AVG({column}),2) FROM onbook_loans', engine).iloc[0,0] / 1000
    ))
    
    fig.update_layout(
        title={
            'text': 'Average Incomes',
            'y': 0.9,
            'x': 0.1,
            'yanchor': 'top',
            'xanchor': 'left',
            'font': {'size': 24, 'color': '#51A1FF'}
        },
        paper_bgcolor='black'
    )
    return fig

@app.callback(
    Output(component_id='dynamic_bar_graph', component_property='figure'),
    Input(component_id='dynamic_bar_graph_menu', component_property='value')
)
def update_bar_graph(column):
    query = pd.read_sql_query(f'select distinct {column} from onbook_loans', engine)
    x_values = query[column].tolist()
    
    if column == 'Gender':
        x_values[2] = 'Unidentified' 
    
    query2 = pd.read_sql_query(f'select distinct {column}, count(*) as Count from onbook_loans group by {column}', engine)
    y_values = []
    for x in x_values:
        match = query2[query2[column] == x]['Count']
        if not match.empty:
            y_values.append(match.iloc[0])
        else:
            y_values.append(0)
    
    fig = go.Figure(go.Bar(x=x_values, y=y_values, marker=dict(color='#51A1FF')))
    
    fig.update_layout(
        title={
            'text': 'Loan Comparison by Category',
            'y': 0.9,
            'x': 0.1,
            'yanchor': 'top',
            'xanchor': 'left',
            'font': {'size': 24, 'color': '#51A1FF'}
        },
        paper_bgcolor='black',
        plot_bgcolor='black',
        xaxis=dict(tickfont=dict(color='#51A1FF')),
        yaxis=dict(tickfont=dict(color='#51A1FF'))
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)