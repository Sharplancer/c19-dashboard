# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plot
from dash.dependencies import Input, Output

external_stylesheets = ['style.css']

dash_app = dash.Dash(__name__)
application = dash_app.server

children = []
children.append(html.H2(children='COVID-19 Forecast for Tufts Medical Center'))
children.append(html.H4(children='Add or remove charts:'))

plot_dict = plot.main()
plot_options = plot_dict.keys()

children.append(
    dcc.Dropdown(id='dropdown',
        options=[{'label': name, 'value': name} for name in plot_options],
        multi=True
    )
)


children.append(html.Div(id='output'))

dash_app.layout = html.Div(
    className='container', children=children
)


@dash_app.callback(Output('output', 'children'), [Input('dropdown', 'value')])
def display_graphs(selected_values):
    graphs = []
    if selected_values != None:
        for value in selected_values:
            graphs.append(dcc.Graph(figure = plot_dict[value]))
        return graphs




if __name__ == '__main__':
    dash_app.run_server(debug=False)