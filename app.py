from dash import Dash, dcc, html, Input, Output, State, DiskcacheManager
import diskcache
import dash_auth
import dash_bootstrap_components as dbc
import base64
import dash
import time
import psql_conn
from datetime import date

import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], background_callback_manager=background_callback_manager)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

language_dropdown = html.Div([
    dcc.Dropdown(['Bengali', 'Odia', 'Maithili'],placeholder="Select Langauge", id='language-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='language-dd-output-container')
])
state_dropdown = html.Div([
    dcc.Dropdown(['West Bengal', 'Odisha', 'Jharkhand','Bihar'], placeholder="Select State", id='state-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='state-dd-output-container')
])


district_dropdown =  html.Div([
    dcc.Dropdown(['Birbhum','Ranchi', 'Bokaro', 'Sambalpur'],placeholder= "Select Distrct", id='district-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='district-dd-output-container')
])

category_dropdown =  html.Div([
    dcc.Dropdown(['Accepted', 'Rejeccted'], placeholder = "Select Category", id='category-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='categoy-dd-output-container')
])

completed_at_datetime = html.Div([dbc.Col([
    html.Div("Completed Between :"),
    html.Div([
    dcc.DatePickerRange(
        id='completed-between-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        #end_date=date(2017, 8, 25)
    ),
    #html.Div(id='output-container-date-picker-range')
])
    ])] ,
    style = {"marginTop":"10px"}

)

verified_at_datetime = html.Div([dbc.Col([
    html.Div("Verified Between :"),
    html.Div([
    dcc.DatePickerRange(
        id='verified-between-picker-range',
        min_date_allowed=date(1995, 8, 5),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        #end_date=date(2017, 8, 25)
    ),
    #html.Div(id='output-container-date-picker-range')
])
    ])] ,
    style = {"marginTop":"10px"}

)

# corresponding audio-file.
encoded_sound = base64.b64encode(open('./Shakira_-_Whenever_Wherever_(ColdMP3.com).mp3', 'rb').read())

report = html.Div("Report Goes Here", id = "result-report")
audio =  html.Audio(id = 'audioplayer',src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()), controls = True, autoPlay = False, style = {"width":"8"})

#----Toast----#
def generate_toast():
    return html.Div(
        [
            dbc.Toast("ye"
                ,
                id="positioned-toast",
                header="Error",
                is_open=False,
                dismissable=True,
                icon="danger",
                duration = 10000,
                # top: 66 positions the toast below the navbar
                style={"position": "fixed", "top": 66, "right": 10, "width": 350},
            ),
        ]
    )


#----Spinner----#
def get_spinner():
    return html.Div(
        [
            dbc.Spinner(color="primary", type="grow",size='md'),
            dbc.Spinner(color="secondary", type="grow"),
            dbc.Spinner(color="success", type="grow",size='md'),
            dbc.Spinner(color="warning", type="grow"),
            dbc.Spinner(color="danger", type="grow",size='md'),
            dbc.Spinner(color="info", type="grow"),
            dbc.Spinner(color="light", type="grow", size = 'md'),
            dbc.Spinner(color="dark", type="grow"),
        ],
        style ={'display':'none','backgroundColor': 'transparent', 'width':8},
        id = 'progress-spinner',

    )

#----Accordian----#
number_of_results = 0
def render_report(report_obj):
    return html.Div(
        [
            html.Ul([html.Li(str(key)+ " : " +str(value)
    )for key,value in report_obj.items()])
        ])

def get_accordian_items(results):

    return  dbc.Accordion([dbc.AccordionItem(
            [   html.Div("Audio goes here"),
                html.Div(render_report(res[1]))
            ],
            title = f"Item {res[0]}",
        )for res in results])

feteched_accordian = html.Div(
     id= 'fetched-audio-row'
)

fetch_button = html.Div(
    [
        html.Div(
            [   #html.P(id="paragraph_id", children=["Button not clicked"]),
                #html.Progress(id="progress_bar", value="0")

            ]
        ),
        html.Div([
        dbc.Button(id="button_id", children="Fetch Results", ),
        dbc.Button(id="cancel_button_id", color = "danger", children="Cancel Running Job!"),],className="d-grid gap-2",)
    ]
)

load_more_button = html.Div(dbc.Button("Load Next...", id="load-more", style = {'display':'none'}),className = "d-grid gap-2 col-6 mx-auto", )
"""
fetched_row = dbc.Row(
    [   audio,
        report
    ], id = 'fetched-audio-row', style={'width': '100%'}
)
"""
app.layout = dbc.Container([
    html.Br(),
    dbc.Card([
        dbc.Row([
            dbc.Col(
        dbc.CardBody([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized')])
           
            ),dbc.Col(dbc.CardImg(
                        src="./static/images/logo.png",
                        className="img-fluid rounded-start",
            ),className="col-md-2"),

        ])],
        color = "primary",inverse=True),
    html.Hr(),

    dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody(html.H2("Filter")),outline=True,color='#0d91fd', inverse = True),html.Br(), language_dropdown, state_dropdown, district_dropdown,category_dropdown, completed_at_datetime,verified_at_datetime, html.Hr(),fetch_button], width = 4),
                dbc.Col( [dbc.Card(dbc.CardBody(html.H2("Results" )),outline = True, color = '#0d91fd', inverse = True),html.Br(),get_spinner(),generate_toast(),feteched_accordian,load_more_button]),
            ],
            align="start",
        ),
],
)

"""
#----Fetch Next Set of Results----#
@dash.callback_context(
    Output('fetched-audio-row','children'),
    Input('load-more','n_clicks'),
    State('language-dropdown','value'), 
    State('state-dropdown','value'), 
    State('district-dropdown','value'), 
    State('category-dropdown','value'),
    State('completed-between-picker-range','start_date'),
    State('completed-between-picker-range','end_date'),
    State('verified-between-picker-range','start_date'),
    State('verified-between-picker-range','end_date'),
    State('fetched-audio-row','children'),
)
def load_next_set_of_data(n_clicks,selected_language, selected_state,selected_district,selected_category, completed_between_start_date, completed_between_end_date, verified_between_start_date, verified_between_end_date, old_row):
    fetched_results = sql_conn.fetch_data( selected_state,selected_district,selected_language, selected_category, n_clicks)
    if len(fetched_results) == 0:
            return [], True, "No Results Found !"
    return old_row+[get_accordian_items(fetched_results)]

    #retunr old_row +  
"""
#----Load more Audio----#

@dash.callback(
    #Output("paragraph_id", "children"),
    Output('fetched-audio-row','children'),
    [Output('positioned-toast','is_open'), 
     Output('positioned-toast','children')],
    #Output('update_progress-spinner', 'style'),
    Input("button_id", "n_clicks"),
    Input("load-more",'n_clicks'),
    State('language-dropdown','value'), 
    State('state-dropdown','value'), 
    State('district-dropdown','value'), 
    State('category-dropdown','value'),
    State('completed-between-picker-range','start_date'),
    State('completed-between-picker-range','end_date'),
    State('verified-between-picker-range','start_date'),
    State('verified-between-picker-range','end_date'),

    background=True,
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
        (Output('progress-spinner','style'),
         {'display':'block','visibility':'visible !important'},
            {'display':'none'}
        ),
        (Output('load-more','style'),
        {'display':'none'},
         {'display':'block'}
        )
    ],
    cancel=Input("cancel_button_id", "n_clicks"),
    #progress=[Output("progress_bar", "value"), Output("progress_bar", "max")],
    prevent_initial_call=True
)
def update_progress(n_clicks,load_more_click,selected_language, selected_state,selected_district,selected_category, completed_between_start_date, completed_between_end_date, verified_between_start_date, verified_between_end_date):


    print(selected_language, selected_state, selected_district, selected_category)
    if selected_language is not None and selected_state is not None and selected_district is not None and selected_category is not None:
        #set_progress((3, 5))i
        dates = []
        for d in [completed_between_start_date, completed_between_end_date, verified_between_start_date, verified_between_end_date]:

            temp_object = date.fromisoformat(d)
            dates.append(temp_object.strftime('%B %d, %Y'))

        print(dates)
        global page_number
        fetched_results, page_number = psql_conn.fetch_data( selected_state,selected_district,selected_language, selected_category,load_more_click)
        #set_progress((5, 5))
        print("result recived")
        if len(fetched_results) == 0:
            return [], True, "No Results Found !"
        return [get_accordian_items(fetched_results)] ,False,""
    else:
        return [] ,True,"Select values for all fields"

    """
    total = 5
    for i in range(total + 1):
        set_progress((str(i), str(total)))
        time.sleep(1)
    return f"Clicked {n_clicks} times"
    """

"""
@app.callback(
    #Output('output','children'),
    #Output('result-report','children'),
    Output('fetched-audio-row','children'),
    Input('language-dropdown','value'), 
    Input('state-dropdown','value'), 
    Input('district-dropdown','value'), 
    Input('category-dropdown','value'),
    #State('output','children'),
    #State('result-report','children'),
    State('fetched-audio-row','children')
)
def more_output(selected_language, selected_state,selected_district,selected_category,old_row):
    if selected_language is not None and selected_state is not None and selected_district is not None and selected_category is not None:
        fetched_results = psql_conn.fetch_data( selected_state,selected_district,selected_language, selected_category)
        return [get_accordian_items(fetched_results)]
"""
"""
@app.callback(
    Output('output','children'),
    [Input('load-new-content','n_clicks')],
    [State('output','children')])
def more_output(n_clicks,old_output):
    if n_clicks==0:
        raise Exception 
    return old_output + [audio]
"""
#----Get Langugae----#
@app.callback(
    Output("language-dd-output-container",'children'),
    Input("language-dropdown","value"),
)
def update_language(value):
    print(value)
    #return f"You have selected {value}"



if __name__ == '__main__':
    app.run_server(debug=True)
