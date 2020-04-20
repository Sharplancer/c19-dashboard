import argparse
import json
from datetime import datetime
import pandas as pd
import re
import plotly.graph_objects as go
import os


def load_output_data(config=None):
    if config is None:
        with open('config.json') as f:
            config = json.load(f)

    output_path = config.pop('output_path')
    num_scenarios = config.pop('num_scenarios')
    time_step_format = config.pop('time_step_format')
    time_delta = parse_time(config.pop('time_delta'))
    first_time_step = config.pop('first_time_step')
    first_time_step_datetime = datetime.strptime(first_time_step, time_step_format)

    summary_files = [(key, val) for (key, val) in config.items() if key.startswith('summary_')]
    all_scenario_dataframes = []
    for scenario_number in range(0, int(num_scenarios)):
        scenario_dataframes = []
        scenario_output_path = output_path + '_{}/'.format(scenario_number)
        for file_type, file_name in summary_files:
            percentile = re.findall('\d*\.?\d+', file_name)[0]

            try:
                df_temp = pd.read_csv(os.path.join(scenario_output_path, file_name))
            except FileNotFoundError:
                df_temp = pd.read_csv(os.path.join(output_path, file_name))
            df_temp['percentile'] = percentile
            df_temp['timestep_formatted'] = df_temp.apply(lambda x: fill_timestep(x.timestep, first_time_step_datetime, time_delta), axis=1)

            if 'upper' in file_type:
                df_temp['bound'] = 'upper'
            elif 'lower' in file_type:
                df_temp['bound'] = 'lower'
            else:
                df_temp['bound'] = 'middle'

            scenario_dataframes.append(df_temp)
        all_scenario_dataframes.append(pd.concat(scenario_dataframes))

    return all_scenario_dataframes, time_step_format


def fill_timestep(timestep, first_time_step_datetime, time_delta):
    return first_time_step_datetime + timestep*time_delta


def parse_time(time_str):
    """
    Parse a time string e.g. (2h13m) into a Panda's timedelta object.

    Modified from virhilo's answer at https://stackoverflow.com/a/4628148/851699

    :param time_str: A string identifying a duration.  (eg. 2h13m)
    :return datetime.timedelta: A Panda's timedelta object
    """
    regex = re.compile(
        r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')

    parts = regex.match(time_str)
    assert parts is not None, "Could not parse any time information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(time_str)
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    return pd.Timedelta(**time_params)


def load_labels():
    with open('labels.json') as f:
        label_dict = json.load(f)

    return label_dict


def make_figure(dfs, labels, time_step_format):
    all_scenario_figures = []
    for df in dfs:
        percentiles = sorted(df.percentile.unique())

        y_cols = list(df.columns)
        y_cols.remove('timestep')
        y_cols.remove('percentile')
        y_cols.remove('timestep_formatted')
        y_cols.remove('bound')

        figures = {}

        # Use the order of the labels.json file for order of figures
        # Much easier to change downstream
        for y in labels.keys():
            fig = go.Figure()

            for p in percentiles:
                df_filtered = df[df['percentile'] == p]

                if df_filtered['bound'].all() == 'lower':
                    fig.add_trace(go.Scatter(
                        x=df_filtered.timestep_formatted,
                        y=df_filtered[y],
                        fill="none",
                        mode='lines',
                        line = dict(color='indigo', width=0),
                        name='%ile: ' + str(float(p))
                    ))

                elif df_filtered['bound'].all() == 'upper':
                    fig.add_trace(go.Scatter(
                        x = df_filtered.timestep_formatted,
                        y = df_filtered[y],
                        fill="tonexty",
                        fillcolor="rgba(75, 0, 130,0.2)",
                        mode='lines',
                        line = dict(color='indigo', width=0),
                        name='%ile: ' + str(float(p))
                    ))

                else:
                    fig.add_trace(go.Scatter(
                        x=df_filtered.timestep_formatted,
                        y=df_filtered[y],
                        fill="tonexty",
                        fillcolor="rgba(75, 0, 130,0.2)",
                        line=dict(color='indigo'),
                        name='%ile: ' + str(float(p))
                    ))

                fig.update_layout(
                    title=labels[y],
                    xaxis_tickformat=time_step_format,
                    xaxis_tickangle=-45,
                    yaxis_title="Patient Count",
                    font=dict(
                        size=12,
                        color="#464646"
                    ),
                    hovermode='x unified',
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_linecolor="#464646",
                    yaxis_linecolor="#464646"
                )

                fig.update_layout(
                    xaxis=dict(
                        # rangeselector=dict(
                        #     buttons=list([
                        #         dict(count=7,
                        #              label="1w",
                        #              step="day",
                        #              stepmode="backward"),
                        #         dict(count=14,
                        #              label="2w",
                        #              step="day",
                        #              stepmode="backward"),
                        #         dict(count=30,
                        #              label="1m",
                        #              step="day",
                        #              stepmode="backward"),
                        #         dict(step="all")
                        #     ]),
                        # ),
                        rangeslider=dict(
                            visible=True
                        ),
                        type="date"
                    )
                )

            figures[labels[y]] = fig

        all_scenario_figures.append(figures)
    return all_scenario_figures


# TODO: Figure out why the graph object height is 100% of view window
def figures_to_html(figs, labels, scenario_title, first_time_step, filename="dashboard.html"):
    dashboard = open(filename, 'w')
    html = '''<html>
           <head>
           <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
           <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>        
           <link rel='stylesheet' type='text/css' href='assets/style.css'>
           </head>
           <body>
           <div class='container'>
           <h2>COVID-19 Forecast for TMC (Experimental Draft)</h2>
           <h1 class="text-center"> {scenario_title} </h1>
           <div class="container-fluid text-left">
           <div class="row content">
           <p> Forecasts started on day: {first_time_step} </p>
           <a name='resources'><h3>Resources</h3></a>
                <ul>
                    <li> Parameters: <a href="params.txt">params.txt</a> </li>
                    <li> Mean CSV summary: <a href="summary-mean.csv">summary-mean.csv</a> </li>
                    <li> Median CSV summary: <a href="summary-percentile=050.00.csv">summary-percentile=050.00.csv</a></li> 
                    <li> 2.5th-perc. CSV summary: <a href="summary-percentile=002.50.csv">summary-percentile=002.50.csv</a></li> 
                    <li> 97.5th-perc. CSV summary: <a href="summary-percentile=097.50.csv">summary-percentile=097.50.csv</a></li> 
                </ul>
           </div>
           <div class="row content">
           <a name='toc'><h3>Plots</h3></a>
           <div class="col-md-12 text-left"> 
           <table class="table" width="100%" border="1">
        '''.format(scenario_title=scenario_title, first_time_step=first_time_step)

    keys = list(labels.keys())
    L = len(keys)
    C = 3 # num cols
    M = L // C # num rows
    list_per_row = [keys[m::M] for m in range(M)]
    key_order = sum(list_per_row, []) # concatenate into flat ordered list
    is_first_col = lambda kk: (kk % C == 0)
    is_last_col = lambda kk: (kk % C == (M-1))
    for kk, key in enumerate(key_order):
        if is_first_col(kk):
            html += "\n<tr>"
        html += '\n    <td class="col-md-4"><a href="#%s">%s</a></td>' % (key, labels[key])
        if is_last_col(kk):
            html += "\n</tr>"
    html += "\n</table></div></div></div>"
    dashboard.write(html + "\n\n")

    inv_labels = dict(zip(labels.values(), labels.keys()))

    for k, v in figs.items():
        inner_html = v.to_html().split("<body>")[1].split("</body>")[0]
        dashboard.write("<a name='%s'><h4>%s</h4>\n" % (inv_labels[k], k))
        dashboard.write("<a href='#toc'>[back to top]</a>\n")
        dashboard.write(inner_html)
    dashboard.write("</div></body></html>" + "\n")


def main():
    with open('config.json') as f:
        config = json.load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dash', default=True)
    for key, val in config.items():
        parser.add_argument('--%s' % key, default=val)
    args = parser.parse_args()
    dash = args.dash

    for key in config:
        if key in args.__dict__:
            config[key] = args.__dict__[key]

    title_list = config['comma_sep_scenario_titles'].split(',')
    scen_id = int(config['scenario_id']) - 1
    if len(title_list) > 0 and scen_id >= 0:
        config['scenario_title'] = title_list[scen_id]

    dfs, time_step_format = load_output_data(dict(**config)) # pass a copy so config cannot be changed as side effect
    labels = load_labels()
    figures = make_figure(dfs, labels, time_step_format)
    
    if dash == True:
        return figures
    else:
        # TODO: Print all figures from different scenarios reasonably
        figures_to_html(figures[0], labels, config['scenario_title'], config['first_time_step'], filename=config['output_html_file'])


if __name__ == "__main__":
    main()

