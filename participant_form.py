from dash import Dash, dcc, html, Input, Output, State
import dash_auth
import dash_bootstrap_components as dbc
import base64
import datetime

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
basic_infomation = html.Div(
    [   
        html.Hr(),
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
        html.Div(dbc.RadioItems(['Male', 'Female','Other'],inline = False, id = 'participant-gender')),
		html.Br(),
        dbc.Label("Enter your Age"),
        dbc.Input(type="number", id="participant-age"),
		html.Br(),
        dbc.Label("Enter your Primary Language (Mother Tongue)"),
        dcc.Dropdown( id="participant-mother-tongue"),
		html.Br(),
		dbc.Label("Please indicate your primary language proficiency"),
		html.Div(dbc.RadioItems(['Speak Only', 'Speak and Read','Speak, Read and Write','Cannot Speak/Read/Write'],inline = False, id = 'participant-language-proficiency')),
		html.Br(),
		dbc.Label("Can You Read and Speak in English?"),
		html.Div(dbc.RadioItems(['Yes', 'No'],inline = False, id = 'participant-english-proficiency')),

    ],
    className="m-3",
)

current_place_of_residence = html.Div(
    [
        html.Hr(),
        html.H5(html.B("Current Place of Residence")),

        html.Br(),
        dbc.Label("Please select State name and District name where you are currently residing"),
        dcc.Dropdown( id = 'participant-state', placeholder = 'Select your State'),
        html.Br(),

        dcc.Dropdown( id = 'participant-district', placeholder = 'Select your District'),
        html.Br(),

    ]
)

education_and_work_experience = html.Div(
    [
        html.Hr(),
        html.H5(html.B("Education and Work Experience")),

        html.Br(),
        dbc.Label("Please select your highest education level "),
        dcc.Dropdown( id = 'participant-education-level', ),
        html.Br(),
        dbc.Label("Please specify your job category"),
        html.Div(dbc.RadioItems(['Freelance', 'Part Time','Full Time', 'Other'],inline = False, id = 'participant-job-category')),
		html.Br(),

        dbc.Label("Please select your occupational domain"),
        dcc.Dropdown( id = 'participant-occupational-domain'),
        html.Br(),

    ]
)


hobbies = html.Div(
    [
        html.Hr(),
        html.H5(html.B("Select 2 hobbies or interest outside of work")),

        html.Br(),
        dbc.Label("Select your First Hobby "),
        dcc.Dropdown( id = 'participant-first-hobby', ),
        html.Br(),
        dbc.Label("Select Yout Second Hobby"),
        dcc.Dropdown( id = 'participant-second-hobby'),
        html.Br(),

    ]
)

intersts = html.Div(
    [
        html.Hr(),
        html.H5(html.B("Select 2 Domains of Interest")),

        html.Br(),
        dbc.Label("Select your First Hobby "),
        dcc.Dropdown( id = 'participant-first-hobby', ),
        html.Br(),
        dbc.Label("Select Yout Second Hobby"),
        dcc.Dropdown( id = 'participant-second-hobby'),
        html.Br(),

    ]
)


product = html.Div(
    [
        html.Hr(),
        html.H5(html.B("Select your favourite category for product review.")),

        html.Br(),
        dbc.Label("Select category "),
        dcc.Dropdown( id = 'participant-product-category', ),
        html.Br(),
        dbc.Label("Select Product"),
        dcc.Dropdown( id = 'participant-product'),
        html.Br(),

    ]
)


upload_form = html.Div([
        html.Hr(),
        html.H5(html.B("Consent Form Upload.")),

        html.Hr(),

        dcc.Upload(
                    id='upload-image',
                    children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                    style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
        html.Div(id='output-image-upload'),
])

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

form = dbc.Form([coordinator_section,basic_infomation, current_place_of_residence, education_and_work_experience, hobbies, product, upload_form], id='form')

app.layout =dbc.Container(

    [
        html.H1('AI4bharat', style = {'color':'red'}),
        html.H1('Maithili Speech Data Participant Collection Form'),
        html.Hr(),
        form,
    ]

)



@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children




if __name__ == '__main__':
    app.run_server(debug=True)
