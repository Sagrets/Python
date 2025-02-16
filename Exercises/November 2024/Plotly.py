import pandas as pd
from dash import Dash, html, dash_table

app = Dash()

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app.layout = [
        html.Div(children='First Data App'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10) 
    ]

if __name__ == '__main__':
    app.run(debug=True)