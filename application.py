# -*- coding: utf-8 -*-
from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plot
from components.charts import chart_panel
from components.controls import control_panel
from components.header import header_panel

dash_app = dash.Dash(__name__)
application = dash_app.server

plot_dicts = plot.main()
plot_options = plot_dicts[0].keys()

dash_app.layout = html.Div(
    className='container', children=[
        header_panel(),
        control_panel(plot_options, len(plot_dicts)),
        chart_panel()
    ]
)


@dash_app.callback(Output('output', 'children'), [Input('chart_selector', 'value'),
                                                  Input('scenario_selector', 'value')])
def display_graphs(selected_charts: List, selected_scenario: int) -> List:
    plot_dict = plot_dicts[selected_scenario]
    graphs = []
    if selected_charts is not None:
        for value in selected_charts:
            graphs.append(dcc.Graph(figure=plot_dict[value]))
        return graphs


if __name__ == '__main__':
    dash_app.run_server(debug=False)
