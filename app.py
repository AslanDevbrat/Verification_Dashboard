from dash import Dash, dcc, html, Input, Output, State
import dash_auth
import dash_bootstrap_components as dbc
import base64
import psql_conn


import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

language_dropdown = html.Div([
    dcc.Dropdown(['Bengali', 'Odia', 'Maithili'],placeholder="Select Langauge", id='language-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='language-dd-output-container')
])
state_dropdown = html.Div([
    dcc.Dropdown(['West Bengal', 'Odisha', 'Jharkhand'], placeholder="Select State", id='state-dropdown', style = {"marginTop":"10px"}),
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


# corresponding audio-file.
encoded_sound = base64.b64encode(open('./Shakira_-_Whenever_Wherever_(ColdMP3.com).mp3', 'rb').read())

report = html.Div("Report Goes Here", id = "result-report")
audio =  html.Audio(id = 'audioplayer',src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()), controls = True, autoPlay = False, style = {"width":"8"})


#----Accordian----#
number_of_results = 0

def get_accordian_items(results):
    
    return  dbc.Accordion([dbc.AccordionItem(
            [   html.Div("AUdio goes here"),
                html.Div(str(res[1]))
            ],
            title = f"Item {res[0]}",
        )for res in results])

feteched_accordian = html.Div(
     id= 'fetched-audio-row'
)
"""
fetched_row = dbc.Row(
    [   audio,
        report
    ], id = 'fetched-audio-row', style={'width': '100%'}
)
"""
app.layout = dbc.Container([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),

    dbc.Row(
            [
                dbc.Col([html.H2("Filter"),html.Br(), language_dropdown, state_dropdown, district_dropdown,category_dropdown], width = 4),
                dbc.Col( [html.H2("Results" ),html.Br(),   feteched_accordian]),
            ],
            align="start",
        ),
],
)



#----Load mor Audio----#

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
    print(selected_language, selected_state, selected_district, selected_category)
    if selected_language is not None and selected_state is not None and selected_district is not None and selected_category is not None:
        
        if  old_row is None:
            fetched_results = psql_conn.fetch_data( selected_state,selected_district,selected_language, selected_category)

            return [get_accordian_items(fetched_results)]

        #return old_row +[audio,html.Div("Report goes here")]
        print(psql_conn.fetch_data( selected_state,selected_district,selected_language, selected_category))
        return old_row +[get_accordian_items(3)]
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
