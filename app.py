from dash import Dash, dcc, html, Input, Output, State, DiskcacheManager
import diskcache
import dash_auth
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import base64
import dash
import time
import psql_conn
from datetime import date ,datetime, timedelta
from flask import request
import pandas as pd

from dash_iconify import DashIconify
import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine


from dash.exceptions import PreventUpdate




# Keep this out of source code repository - save in a file or a database

df = pd.read_csv("./filters.csv")

VALID_USERNAME_PASSWORD_PAIRS = {
    'CF': 'world',
    'AF':'world'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], background_callback_manager=background_callback_manager)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
print(auth)
def get_themeicon(icon_name):
    return dmc.ThemeIcon(
        size="lg",
        color="orange",
        variant="light",
        radius = "lg",
        children=DashIconify(icon=icon_name ,width=25)
    )

print(df['Language'].dropna().unique())
language_dropdown = html.Div(
    [
        dmc.Select(
            withAsterisk = True,
            label="Select Language",
            radius = 100,
            placeholder="Select one",
            id="language-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("material-symbols:location-on-outline-rounded"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data= df['Language'].dropna().unique(),
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)



state_dropdown = html.Div(
    [
        dmc.Select(
            withAsterisk = True,
            transition = 'skew-down',
            label="Select State",
            radius = 100,
            placeholder="Select one",
            id="state-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("material-symbols:location-on-outline-rounded"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data= [],
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)

 



district_dropdown =  html.Div(
    [
        dmc.Select(
            withAsterisk = True,
            label="Select District",
            radius = 100,
            placeholder="Select one",
            id="district-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("material-symbols:location-on-outline-rounded"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data=[
                'Birbhum','Ranchi', 'Bokaro', 'Sambalpur'
                ],
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)




category_dropdown =  html.Div(
    [
        dmc.Select(
            withAsterisk = True,
            label="Select Category",
            radius = 100,
            placeholder="Select one",
            id="category-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("radix-icons:magnifying-glass"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data=[
                'Accepted', 'Rejected'
                ],
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)

date_picker = html.Div(
    [
        dmc.DateRangePicker(
            withAsterisk = True,
            id="date-range-picker",
            icon= get_themeicon("bi:calendar-date"),
            #label="Date Range",
            description="Select a Date Range",
            minDate=date(2020, 8, 5),
            value=[date(2022,1,1), datetime.now().date()],
            style={"width": "load_more_buttono"},
        ),
        dmc.Space(h=10),
        dmc.Text(id="selected-date-date-range-picker"),
    ],
style = {"marginTop":"10px"}

)
"""
html.Div([dbc.Col([
    #html.Div("Completed Between :"),
    html.Div([
    dcc.DatePickerRange(
        id='date-range-picker',
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
"""
"""
html.Div(
    [
        dmc.DateRangePicker(
            id="date-range-picker",
            label="Date Range",
            description="You can also provide a description",
            minDate=date(2020, 8, 5),
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
            style={"width": 330},
        ),
        dmc.Space(h=10),
        dmc.Text(id="selected-date-date-range-picker"),
    ]
)
"""
"""
html.Div(
    [
        dmc.DatePicker(
            id="date-range-picker",
            label="Start Date",
            description="You can also provide a description",
            minDate=date(2020, 8, 5),
            value=datetime.now().date(),
            style={"width": 200},
        ),
        dmc.Space(h=10),
        dmc.Text(id="selected-date"),
    ]
)
"""
"""
html.Div(
    [
        dmc.DateRangePicker(
            withAsterisk = True,
            id="date-picker",
            icon= get_themeicon("bi:calendar-date"),
            #label="Date Range",
            description="Select a Date Range",
            minDate=date(2020, 8, 5),
            value=[datetime.now().date(), datetime.now().date() + timedelta(days=5)],
            style={"width": "auto"},
        ),
        dmc.Space(h=10),
        #dmc.Text(id="selected-date-date-range-picker"),
    ],
style = {"marginTop":"10px"}

)
"""
date_dropdown =  html.Div(
    [
        dmc.Select(
            withAsterisk = True,
            label="Select Date filter",
            radius = 100,
            placeholder="Select one",
            id="date-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("radix-icons:magnifying-glass"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data=[
                'Completed Between', 'Verified Between'
                ],
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
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

#disableChevronRotation
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

badge_color = {
    'sst': 'gray', 'noise': 'red', 'chatter': 'pink', 'comments': '', 'decision': 'reject', 'book_read':'grape', 'off_topic': 'violet', 'low_volume': 'indigo', 'stretching': 'blue', 'long_pauses': 'lime', 'unclear_audio': 'yellow', 'reading_prompt': 'orange', 'mispronunciation': 'green', 'repeating_content': 'brown','bad_extempore_quality':'bright-pink',
    'bad_read_quality':'ocean-blue'
}
def render_report(report_obj):
    return html.Div(
        [
            html.Ul([html.Li(str(key)+ " : " +str(value)
    )for key,value in report_obj.items()])
        ])

def create_accordion_content(content):
    return dmc.AccordionPanel(render_report(content))


def create_accordion_label(label, audio_name, description):
    print("creating labels")
    return dmc.AccordionControl([html.Div(audio_name),dmc.Group([dmc.Badge(key, color = badge_color[key]) if value == True else ""for key,value in label.items()]), dmc.Text(description, size="sm", weight=400, color="dimmed"),])


def get_accordian(results):
    return dmc.Accordion(
        disableChevronRotation = False,
        chevronPosition="right",
        variant="contained",
        children=[
            dmc.AccordionItem(
                [
                    create_accordion_label(
                        res[1], res[0], res[1]['comments']
                    ),
                    #create_accordion_content(res[1]),
                ],
                value=res[0],
            )
            for res in results
        ],
    )

def get_accordian_items(results):

    return  html.Div(
        dmc.Accordion([dmc.AccordionItem(
            #create_accordion_content
            #dmc.AccordionControl([f"Item {res}", dmc.Badge("New")]),
            dmc.AccordionPanel(
            [   html.Div("Audio"),
                html.Div(render_report(res[1])),


            ],
value = f"{res[0]}"
            ),


        )for res in results ], dbc.Badge("New")
        ),
        style={"maxHeight": "500px", "overflow": "scroll"}
    )

feteched_accordian = html.Div(
     id= 'fetched-audio-row',
    style={"maxHeight": "400px", "overflow": "scroll"}
)

fetch_button = html.Div(
    [
        html.Div(
            [   #html.P(id="paragraph_id", children=["Button not clicked"]),
                #html.Progress(id="progress_bar", value="0")

            ]
        ),
        html.Div([
            #audio,
        dbc.Button(id="button_id", children="Fetch Results", ),
        dbc.Button(id="cancel_button_id", color = "danger", children="Cancel Running Job!"),],className="d-grid gap-2",)
    ]
)

load_more_button = html.Div(dbc.Button("Load Next...", id="load-more", style = {'display':'none'}),className = "d-grid gap-2 col-6 mx-auto", style={'margin-top':'8'})
"""
fetched_row = dbc.Row(
    [   audio,
        report
    ], id = 'fetched-audio-row', style={'width': '100%'}
)
"""
def get_card(title, content):
    return dmc.Card(
        children = [
            dmc.Text(html.H4(title), color = "white")
        ],
    withBorder=True,
    shadow="sm",
    radius="lg",
    bg = '#ffad13'
    )


def get_dropdows():

    language = df['Language'].unique()
    state = df['State/UT'].unique()


tabs = dmc.Tabs(
    [
        dmc.TabsList(
            [
                dmc.Tab(
                    "Verification",
                    icon=get_themeicon('ic:outline-domain-verification'),
                    value="verification",
                    color= '#ffad13'
                ),
                dmc.Tab(
                    "Analytics",
                    icon=get_themeicon('mdi:graph-box-outline'),
                    value="analytics",
                ),
            ]
        ),
    ],
    value="verification",
    id = 'tabs-example'
)


verification_component = dbc.Row(
            [
                dbc.Col([get_card("Filter",""),html.Br(), language_dropdown, state_dropdown, district_dropdown,category_dropdown, date_dropdown,date_picker, html.Hr(),fetch_button], width = 4),
                dbc.Col( [get_card("Results",""),html.Br(),get_spinner(),generate_toast(),feteched_accordian,html.Hr(),]),
            ],
            align="start",
        )

analytics_component =  html.Iframe(src="https://www.ons.gov.uk/visualisations/dvc914/map/index.html",
                style={"height": "1000px", "width": "100%"})

common_tab = dbc.Container([
    html.Br(),
    
    dmc.Card([
        dbc.Row([
            dbc.Col(
        dmc.Text([
    html.H1('Welcome to the app'),
    html.H3('You AccordionItem successfully authorized')], 
        color="white"
        )
           
            ),dbc.Col(dbc.CardImg(
                        src="./static/images/logo.png",
                        className="img-fluid rounded-start",
            ),className="col-md-2"),

        ])],withBorder=True,
    shadow="sm",
    radius="md",
    bg = 'orange'
        ),
    html.Hr(),
    tabs,
    html.Br(),
    html.Div(
        verification_component,
    id = 'main-content'
    )
],

)

app.layout = html.Div(common_tab, style ={'backgroundColor':'#fffce5'} )
"""
@app.callback(
    Output('language-dropdown','data'),
    Input('language-dropdown','value')
)
def set_language(val):
    df = pd.read_csv('./filters.csv')
    return df['Language'].unique()
"""
@app.callback(
    Output('state-dropdown','data'),
    Input('language-dropdown','value')
)
def get_state(seleted_language):
    username = request.authorization['username']
    #print(df[df['User']== username]['State/UT'].dropna().unique())
    return sorted(df[df['User']== username]['State/UT'].dropna().unique())

@app.callback(
    Output('district-dropdown','data') ,
    Input('state-dropdown','value')
)
def set_disrict_value(selected_state): 

    return sorted(df[df['State/UT'] == selected_state]['District'].dropna().values.tolist())


@app.callback(
    Output("selected-date-date-range-picker", "children"),
    Input("date-range-picker", "value"),
)
def update_output(dates):
    prefix = "You have selected: "
    if dates:
        return prefix + "   -   ".join(dates)
    else:
        raise PreventUpdate



@app.callback(Output("main-content", "children"), Input("tabs-example", "value"))
def render_content(active):
    if active == "verification":
        return verification_component
    else:
        return analytics_component

#----Load more Audio----#

@dash.callback(
    #Output("paragraph_id", "children"),
    Output('fetched-audio-row','children'),
    [Output('positioned-toast','is_open'), 
     Output('positioned-toast','children')],
    #Output('update_progress-spinner', 'style'),
    Input("button_id", "n_clicks"),
    #Input("load-more",'n_clicks'),
    State('language-dropdown','value'), 
    State('state-dropdown','value'), 
    State('district-dropdown','value'), 
    State('category-dropdown','value'),
    State('date-dropdown','value'),
    State('date-range-picker','value'),
    #State('date-range-picker','end_date'),
    #State('date-range-picker','start_date'),
    #State('verified-between-picker-range','end_date'),

    background=True,
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
        (Output('progress-spinner','style'),
         {'display':'block','visibility':'visible !important'},
            {'display':'none'}
        ),
    ],
    cancel=Input("cancel_button_id", "n_clicks"),
    #progress=[Output("progress_bar", "value"), Output("progress_bar", "max")],
    prevent_initial_call=True
)
def update_progress(n_clicks,selected_language, selected_state,selected_district,selected_category, date_category, dates):


    print(selected_language, selected_state, selected_district, selected_category)
    if selected_language is not None and selected_state is not None and selected_district is not None and selected_category is not None:
        #set_progress((3, 5))i
        #dates = []
        """
        for d in [completed_between_start_date, completed_between_end_date]:

            temp_object = date.fromisoformat(str(d))
            dates.append(temp_object.strftime('%B %d, %Y'))

        print(dates)
        """
        #print(date)
        #global page_number
        #print(dates)
        fetched_results = psql_conn.fetch_data( selected_state,selected_district,selected_language, selected_category, date_category, dates[0], dates[1])
        #print(fetched_results[0][1])
        #set_progress((5, 5))
        print("result recived")
        
        if len(fetched_results) == 0:
            return [], True, "No Results Found !"
        return [get_accordian(fetched_results)] ,False,""
    else:
        return [] ,True,"Select values for all fields"

if __name__ == '__main__':
    app.run_server(debug=True)
