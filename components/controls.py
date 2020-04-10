from typing import Set

import dash_core_components as dcc
import dash_html_components as html


def control_panel(plot_options: Set, num_scenarios: int) -> html.Div:
    return html.Div(id='control_panel', className='row',
                    children=[html.Div(className='column',
                                       children=[chart_selector(plot_options),
                                                 scenario_selector(num_scenarios)])])


def chart_selector(plot_options: Set) -> html.Div:
    return html.Div(id='chart_selector_div', children=[
        html.H4(children='Add or remove charts:'),
        dcc.Dropdown(id='chart_selector',
                     options=[{'label': name, 'value': name} for name in plot_options],
                     multi=True)
    ])


def scenario_selector(num_scenarios: int) -> html.Div:
    options = [{'label': 'Scenario {}'.format(i), 'value': i} for i in range(num_scenarios)]

    return html.Div(id='scenario_selector_div', children=[
        html.Label(children='Select a scenario'),
        dcc.RadioItems(
            id='scenario_selector',
            options=options,
            value=0,
            labelStyle={'display': 'inline-block'}
        )
    ])
