from dash import Dash, dcc, html, Input, Output, State
import dash_auth
import dash_bootstrap_components as dbc
import base64


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#----Coordinator-Section----#
coordinator_section = html.Div(
    [   html.H5(html.B("Coordinator Section")),
        html.Br(),
        dbc.Label("Coordinator Name"),
        dbc.Input(type="text", id="coordinator-name", placeholder="Enter Coordinator Name"),
        html.Br(),
        #html.Div(style={'margin':'12'}),
        dbc.Label("Coordinator Phone Number"),
        dbc.Input(type="number", id="coordinator-phone-number", placeholder="Enter Coordinator's Phone Number"),

    ],
    className="m-3",
)

#----Basic Information----#
basic_infomation = dbc.Row(
    [
        html.H5(html.B("Basic Information")),
        html.Br(),
        dbc.Label("Enter Your Full Name"),
        dbc.Input(type="text", id="participant-name" ),
        html.Br(),
        dbc.Label("Enter your 10-Digit Phone Number"),
        dbc.Input(type="number", id="participant-phone-number",),
        html.Br(),
        dbc.Label("Please enter your Email-Id"),
        dbc.Input(type="email", id="participant-email-id"),
        html.Br(),
        html.Div("Please select your Gender"),
        dcc.RadioItems(['Male', 'Female','Other'],inline = False)



    ],
    className="m-3",
)



app.layout =dbc.Container(

    [
        html.H1('AI4bharat', style = {'color':'red'}),
        html.H1('Maithili Speech Data Participant Collection Form'),
        html.Hr(),
        html.Div([
            coordinator_section,
            html.Hr(),
            basic_infomation,
        ])
    ]

)

if __name__ == '__main__':
    app.run_server(debug=True)
