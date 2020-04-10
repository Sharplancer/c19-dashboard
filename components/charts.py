import dash_html_components as html


def chart_panel() -> html.Div:
    return html.Div(className='row', children=[html.Div(id='output', className='column')])
