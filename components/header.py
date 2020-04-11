import dash_html_components as html


def header_panel() -> html.Div:
    return html.Div(className='row', children=[html.Div(className='column', children=[
        html.H2(children='COVID-19 Forecast for TMC (Experimental Draft)')
    ])])

