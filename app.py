import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime as dt
import plotly.figure_factory as ff
import colorlover as cl

app = dash.Dash()

df = pd.read_csv("data.csv")
df.fillna(df.mean(), inplace=True)

def datetime(str):
    date_time = dt.strptime(str, '%d-%m-%Y')
    return date_time

df["DATE"] = df["DATE"].apply(datetime)

options = []

cols = [ dict(label = "Precipitation", value = "PRCP"), dict(label = "Max Temp", value = "TMAX")]

for option in df["NAME"].unique():
    mydict = {}
    mydict['label'] = option
    mydict['value'] = option
    options.append(mydict)

app.layout = html.Div(html.Div([
                    html.H1("Weather Stats", style={"paddingTop":"1%", "paddingLeft": "2%", 'fontSize': 34, 'lineHeight': 1.5, 'font-family': "'Segoe UI',Roboto, Arial, sans-serif"}),
                    html.Hr(style={"width": "97%"}),
                    html.Div([
                    html.Label('Select a City: ', style={'fontSize': 16, 'lineHeight': 1.5, 'font-family': "Helvetica Neue, Helvetica, Arial, sans-serif"}),
                    dcc.Dropdown(
                                id = 'cities-ddl',
                                options=options,
                                value=['New York', 'New Delhi'],
                                multi=True,
                                style={'padding': '0.5%'}
                            )
                    ],
                                style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '62%', "marginLeft":"1%"}
                    ),
                    html.Div([
                        html.Label('Select a Date Range: ', style={'fontSize': 16, 'lineHeight': 1.5, 'font-family': "Helvetica Neue, Helvetica, Arial, sans-serif"}),
                        dcc.DatePickerRange(
                                 id='date-picker',
                                 min_date_allowed = dt(2010, 1, 1),
                                 max_date_allowed =  dt(2019, 4, 22),
                                 start_date = dt(2019, 1, 1),
                                 end_date = dt(2019, 4, 22)
                            )
                        ],
                        style = {'display': 'inline-block', 'verticalAlign': 'top', 'width': '25%', 'marginLeft': '2%'}
                    ),
                    html.Div([
                    dcc.RadioItems(
                        id = 'radio-val',
                        options=cols,
                        value='PRCP'
                    )],
                    style = {'display': 'inline-block',"width": "9%", 'marginTop': '1.5%'}
                    ),
                    dcc.Tabs(id="tabs", children=[
                        dcc.Tab(label='Line Chart', children=[
                            dcc.Graph( id = 'line-chart')
                            ]),
                        dcc.Tab(label='Bar Chart', children=[
                            dcc.Graph( id = 'heatmap')
                            ])
                        ])

],
style = {"width": "95%", "margin": "0 auto", "boxShadow": "4px 4px 5px 2px rgba(0, 0, 255, .2)"}
),
style = {"backgroundColor": "white"}
)

@app.callback(Output('line-chart', 'figure'),
              [Input('cities-ddl', 'value'),
               Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date'),
               Input('radio-val', 'value')
               ])
def update_graph(cities, start_date, end_date, radio):
    start = dt.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    print(radio)
    for city in cities:
        data = df[(df["DATE"].between(start, end)) & (df["NAME"] == city)]
        traces.append({'x': data['DATE'], 'y': data[radio], 'name': city})

    # df = web.DataReader(stock_ticker, 'iex', start, end)
    fig = {
            'data': traces,
            'layout': {'title': cities,
                    'plot_bgcolor': '#EEEEEE',
                    'paper_bgcolor': '#EEEEEE',
                    'xaxis': dict(
                                rangeselector=dict(
                                    buttons=list([
                                        dict(count=1,
                                             label='1m',
                                             step='month',
                                             stepmode='backward'),
                                        dict(count=6,
                                             label='6m',
                                             step='month',
                                             stepmode='backward'),
                                        dict(count=1,
                                            label='YTD',
                                            step='year',
                                            stepmode='todate'),
                                        dict(count=1,
                                            label='1y',
                                            step='year',
                                            stepmode='backward'),
                                        dict(step='all')
                                    ])
                                ),
                                rangeslider=dict(
                                    visible = True
                                ),
                                type='date'
                            ),
                    'yaxis': {"title": radio}
                    }
    }

    return fig




@app.callback(Output('heatmap', 'figure'),
              [Input('cities-ddl', 'value'),
               Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date'),
               Input('radio-val', 'value')
               ])
def update_graph(cities, start_date, end_date, radio):
    start = dt.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    color = cl.scales['11']['qual']['Paired']
    print(radio)
    i = 1
    for city in cities:
        data = df[(df["DATE"].between(start, end)) & (df["NAME"] == city)]
        traces.append(go.Bar(x = data['DATE'], y= data[radio], name = city, marker = {'color': color[i]}))
        i = i + 2

    layout = go.Layout(title = radio, plot_bgcolor = '#EEEEEE', paper_bgcolor = '#EEEEEE',
                        xaxis = dict(
                                    rangeselector=dict(
                                        buttons=list([
                                            dict(count=1,
                                                 label='1m',
                                                 step='month',
                                                 stepmode='backward'),
                                            dict(count=6,
                                                 label='6m',
                                                 step='month',
                                                 stepmode='backward'),
                                            dict(count=1,
                                                label='YTD',
                                                step='year',
                                                stepmode='todate'),
                                            dict(count=1,
                                                label='1y',
                                                step='year',
                                                stepmode='backward'),
                                            dict(step='all')
                                        ])
                                    ),
                                    rangeslider=dict(
                                        visible = True
                                    ),
                                    type='date'
                                ),
                        yaxis = {"title": radio})

    fig = go.Figure(data = traces, layout = layout)

    return fig

if __name__ == "__main__":
    app.run_server()
