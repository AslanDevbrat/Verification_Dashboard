from dash import Dash, dcc, html, Input, Output, State
import dash_auth
import dash_bootstrap_components as dbc
import base64
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
    dcc.Dropdown(["Bengali", "Odia", "Maithili"], id='language-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='dd-output-container')
])
"""
dbc.DropdownMenu(
    label="Language",
    children=[
        dbc.DropdownMenuItem("Bengali"),
        dbc.DropdownMenuItem("Odia"),
        dbc.DropdownMenuItem("Maithili"),
    ],
)
"""
state_dropdown = html.Div([
    dcc.Dropdown(["West Bengal", "Odisha", "Jharkhand"], id='state-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='dd-output-container')
])


district_dropdown =  html.Div([
    dcc.Dropdown(["Ranchi", "Bokaro", "Sambalpur"], id='district-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='dd-output-container')
])


# corresponding audio-file.
encoded_sound = base64.b64encode(open('./Shakira_-_Whenever_Wherever_(ColdMP3.com).mp3', 'rb').read())

audio = html.Div([
    html.Audio(id = 'audioplayer',src='data:audio/mpeg;base64,{}'.format(encoded_sound.decode()), controls = True, autoPlay = False, style = {"width":"100%"}) 
]
)
category_dropdown =  html.Div([
    dcc.Dropdown(["Accepted", "Rejeccted"], id='category-dropdown', style = {"marginTop":"10px"}),
    html.Div(id='dd-output-container')
])

app.layout = dbc.Container([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),

    dbc.Row(
            [
                dbc.Col([html.Div("Filter"), state_dropdown, district_dropdown, language_dropdown,category_dropdown], width = 4),
                dbc.Col( [html.Div("Results" ), html.Div( 
                    id = "output", 
                    children= [audio]
                )
                ], width =8),
                html.Button("Load more",id='load-new-content',n_clicks=0)
            ],
            align="start",
        ),
],
    className = "pad-row"
)



@app.callback(
    Output('output','children'),
    [Input('load-new-content','n_clicks')],
    [State('output','children')])
def more_output(n_clicks,old_output):
    if n_clicks==0:
        raise PreventUpdate
    return old_output + [audio]

if __name__ == '__main__':
    app.run_server(debug=True)
