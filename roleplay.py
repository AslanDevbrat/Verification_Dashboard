import dash
#from dash.dependencies import Input, Output
from dash import html,DiskcacheManager, State, Input, Output
import diskcache
import dash_bootstrap_components as dbc
from datetime import datetime

import time
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import tarfile
import requests
import io
import os
import base64
import pandas as pd

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

df = pd.read_csv('./roles.tsv',sep='\t')
app = dash.Dash(background_callback_manager=background_callback_manager)


def get_themeicon(icon_name):
    return dmc.ThemeIcon(
        size="lg",
        color="orange",
        variant="light",
        radius = "lg",
        children=DashIconify(icon=icon_name ,width=25)
    )

role_category_dropdown = html.Div(
    [
        dmc.Select(
            withAsterisk = True,
            label="Select Roleplay Category",
            radius = 100,
            placeholder="Select one",
            id="roleplay-category-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("material-symbols:location-on-outline-rounded"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data= ['General','State','District'],
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)


role_sub_category_dropdown = html.Div(
    [
        dmc.Select(
data =[],
            withAsterisk = True,
            label="Select One",
            radius = 100,
            placeholder="Select one",
            id="roleplay-sub-category-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("material-symbols:location-on-outline-rounded"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            #data= ['General','State','District'],
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px", 'style':'block' }
)

topic_dropdown = html.Div(

    [   dmc.Text("Topic", size = 'lg'),
        dmc.Select(
            data =[],
            withAsterisk = True,
            label="Select Topic of Discussion ",
            radius = 100,
            placeholder="Select one",
            id="topic-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("icon-park-outline:topic"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)


call_button = dmc.Button("Call/Recall", color = "orange", id = "call-button", radius = 100)

fetch_button = dmc.Button("Fetch", color = "orange", id = "fetch-button", radius = 100,style={'display':'none'})



recording_timeline = html.Div(dmc.Timeline(
    id = 'call-timeline',
    style={'display':'none', 'visibility':'hidden'},
    active=0,
    bulletSize=15,
    lineWidth=2,
    children=[
        dmc.TimelineItem(
            id ='call-initiated-timeline',
            title="Call Initiated",
            color = 'orange',

            children=[
                dmc.Text(
                    "Following is your S-Id",
                    color="dimmed",
                    size="sm",
                ),
                dmc.Text(

                    color="dimmed",
                    size="sm",
                    id = "sid"
                )
            ],
        ),
                   ],
),
#style = {'display':'none'}
)
def get_speaker_detail_section(number_of_speaker):
    return html.Div(
        [
            html.Div(
                [
                    dmc.Text(f"Speaker {num} Details", size = 'lg'),
                    dmc.Grid(
                        children=[
                            dmc.Col(dmc.TextInput(label=f"Participant Name",
                                                id = f'participant-{num}-name',
                                                  radius = 100,
                                                  placeholder ="Enter Name",
                                                  icon= get_themeicon("icon-park-outline:edit-name"), ) , span=6),
                            dmc.Col( dmc.TextInput(label=f"Phone Number",
                                                id = f'participant-{num}-phone-number',
                                                   type = 'number',
                                                  radius = 100,
                                                  placeholder ="Enter Number",
                                                   icon= get_themeicon("material-symbols:phone-enabled-outline"),) , span=6)
                                                   ],
                        gutter="xl",
                    ),
                    html.Div(
    [
        dmc.Select(
data =[],
            withAsterisk = True,
            label="Select Role",
            radius = 100,
            placeholder="Select one",
            id=f"participant-{num}-role-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("carbon:user-role"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            style={"width": 'auto', "marginBottom": 10},
        ),
        #dmc.Text(id="selected-value"),
    ],
    style = {"marginTop":"10px"}
)

                ]
            )for num in range(1,number_of_speaker)
        ]
    )
audio_player = html.Div(
    [
        html.Div(
        #     [
        #         # html.Div(id = 'accordian-item'),
        #         # html.Audio(id = 'player', controls = True, autoPlay = False, style = {"width":"8"})
        #             # dash_player.DashPlayer(
        #             #     id="player",
        #             #     # url='data:audio/mpeg;base64,{}'.format(get_audio_data().decode()),
        #             #     controls=True,
        #             #     width="100%",
        #             #     height='50px',
        #             #     playing=False,
        #             #     playsinline=False,
        #             #     # style={"background":"lightgrey"}
        #             # ),
        #    ],
            id='player_container',
        ),
    ]
)



role_sub_category_district_dropdown = dmc.Grid(
    id = 'state-district-dropdown',
    children = [
        dmc.Col(dmc.Select(
            withAsterisk = True,
            label="Select State",
            radius = 100,
            placeholder="Select one",
            id=f"state-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("carbon:user-role"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data =[],
            style={"width": 'auto', "marginBottom": 10},
        ), span = 6),
        dmc.Col(dmc.Select(
            withAsterisk = True,
            label="Select District",
            radius = 100,
            placeholder="Select one",
            id=f"district-dropdown",
            #value="ng",
            searchable = True,
            icon= get_themeicon("carbon:user-role"),
            #DashIconify(icon="radix-icons:magnifying-glass"),
            rightSection=DashIconify(icon="radix-icons:chevron-down"),
            nothingFound = "No Options Found!",
            data =[], 
            style={"width": 'auto', "marginBottom": 10},
        ), span = 6)
    ],
    style = {'display':'none'}
)


toast = html.Div(
        [
            dbc.Toast(
                "ERrOR",
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
error_toast = html.Div(
        [
            dbc.Toast(
                id="run_serveror-toast",
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

notification = html.Div(
    [
        html.Div(id="notifications-container",children = [ dmc.Notification(
        title="Error!",
        id="simple-notify",
        action="hide",
        #message="Notifications in Dash, Awesome!",
        color = 'red',
        message = "",
        icon=DashIconify(icon="ic:round-error"),
    )] ),
        #dmc.Button("Show Notification", id="notify"),
    ]
)

number_notification = html.Div(
    [
        html.Div(id="number_check",children = [ dmc.Notification(
        title="Error!",
        id="number-verify-notify",
        action="hide",
        #message="Notifications in Dash, Awesome!",
        color = 'red',
        message = "",
        icon=DashIconify(icon="ic:round-error"),
    )] ),
        #dmc.Button("Show Notification", id="notify"),
    ]
)
main_card = html.Div(
    dbc.Row(
    dmc.Card(
        children = [
            dmc.Text(
            "It might be the case that call is not getting processed which is because the phone number is on DND. For those participants, please make two calls from each of their mobile to 08047361850 and 08035240690 and then proceed with the calling procedure. Thanks!",
            size="sm",
            color="dimmed",

            
        ),  
            role_category_dropdown,
            role_sub_category_dropdown,
            role_sub_category_district_dropdown,
            html.Br(),
            get_speaker_detail_section(3),
            html.Br(),
            topic_dropdown,
            html.Br(),
            call_button,
            html.Br(),
            html.Hr(),
            recording_timeline,
            html.Hr(),
            fetch_button,
            html.Br(),
            audio_player,
            toast,
            error_toast,
            notification,
            number_notification
        ],withBorder=True,
            shadow="sm",
        style = {'width':'auto', 'margin-left':'10px', 'margin-right':'10px'}
    ),
justify="center", align="center", className="h-50"

    #style ={'align':'center','width':'100vh'}
),)
app.layout = dmc.NotificationsProvider(html.Div(
    [
        main_card,
        
    ]

),position = 'top-right' )


file_path = '/data/bucket'
os.makedirs(file_path,exist_ok= True)
def get_file(filename):
    if os.path.exists(f'{file_path}/{filename}'):
        with open(f'{file_path}/{filename}','rb') as reader:
            encoded_sound = base64.b64encode(reader.read())
    else:
        if len(filename) > 15+4:
            data = requests.get(url=f'https://ai4bdmukarya.blob.core.windows.net/role-play-convs/{filename.split(".")[0]}.wav?sp=r&st=2023-03-22T14:16:18Z&se=2025-12-31T22:16:18Z&spr=https&sv=2021-12-02&sr=c&sig=KkW8E8KRNRmCW6%2FUOhEvJ4FDusgumKBQBefQbXRPOBM%3D')
            with open(f'{file_path}/{filename}','wb') as writer:
                writer.write(data.content)
            encoded_sound = base64.b64encode(data.content)
        else:
            data = requests.get(url=f'https://ai4bdmukarya.blob.core.windows.net/microtask-assignment-output/{filename.split(".")[0]}.tgz?sp=r&st=2023-03-21T04:41:45Z&se=2026-01-01T12:41:45Z&spr=https&sv=2021-12-02&sr=c&sig=0I5haNNC%2FufmGgJLGW11uLLK7c2TdaPbFh5iB%2BFpvYg%3D')
            # print(data.status_code,data.content)
            if data.status_code == 200:
                io_bytes = io.BytesIO(data.content)
                tar = tarfile.open(fileobj=io_bytes, mode='r:gz')
                with open(f'{file_path}/{tar.firstmember.name}','wb') as writer:
                    f1 = tar.extractfile(tar.firstmember)
                    writer.write(f1.read())
                f = tar.extractfile(tar.firstmember)
                encoded_sound = base64.b64encode(f.read())
    return encoded_sound

"""
@dash.callback(
    Output("notifications-container", "children"),
    Input("notify", "n_clicks"),
    prevent_initial_call=True,
)
def show(n_clicks):
    return dmc.Notification(
        title="Hey there!",
        id="simple-notify",
        action="show",
        message="Notifications in Dash, Awesome!",
        icon=DashIconify(icon="ic:round-celebration"),
    )

"""


@dash.callback(
            Output("simple-notify","action"),
            Output("simple-notify", 'message'),
            Output("call-timeline", "active"),
           Output("fetch-button",'style'),
           Output('call-timeline','style'),
           Output('sid','children'),
           Input("call-button", "n_clicks"),
           State("roleplay-category-dropdown",'value'),
           State("roleplay-sub-category-dropdown",'style'),
           State("roleplay-sub-category-dropdown",'value'),
            State("state-dropdown",'style'),
            State("state-dropdown", 'value'),
            State("district-dropdown",'style'),
            State("district-dropdown",'value'),
           State("participant-1-name",'value'),
           State("participant-1-phone-number",'value'),
           State("participant-1-role-dropdown",'value'),
           State("participant-2-name",'value'),
           State("participant-2-phone-number",'value'),
           State("participant-2-role-dropdown", 'value'),
           State('topic-dropdown','value'),
           prevent_initail_call = True 
)
def initiate_call(n_clicks,roleplay_category,roleplay_sub_category_style, roleplay_sub_category, state_dropdown_style, state_dropdown, district_dropdown_style, district_dropdown, name_1, number_1,role_1, name_2, number_2,role_2, topic ):
    #print(n_clicks)
    #print(roleplay_category_style)
    if n_clicks == None:
        return  'hide' ,'',0, {'display':'none'}, {'display': 'none'}, ""

    if roleplay_category == "General":
        pass
    elif roleplay_category == "State":
        if roleplay_sub_category_style['display'] != 'none' and roleplay_sub_category == None:
            return  'show',"Selcet state" ,0, {'display':'none'}, {'display': 'none'}, ""
    elif roleplay_category == "District":
        print(district_dropdown_style)
        if ( state_dropdown == None) or ( district_dropdown == None) :
            return 'show',"Select both district and state",0, {'display':'none'}, {'display': 'none'}, ""
 
    if len(name_1) == 0 or len(number_1) !=10 or role_1 == None or len(name_2) == 0 or len(number_2) !=10 or role_2 == None in topic == None:
        print("WTF") 
        return 'show','Select all fields' ,0, {'display':'none'}, {'display': 'none'}, ""
    else:
        print(name_1,number_1,role_1,name_2,number_2,role_2,topic)
        """
        url = "https://kpi.knowlarity.com/Basic/v1/account/call/makecall"
        payload = {
                    "k_number": "+919513248817",
                    "agent_number": "+91"+number_1,
                    "customer_number": "+91"+number_2,
                    "caller_id": "+918035240690"
        }
        headers = {
        'Authorization': KN_AUTH,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': KN_API_KEY,
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        print(response.json())
        sid = response.json()['success']['call_id']
        return_response = response.json()
        return_response['Call'] = {"Sid":sid}

        """
        return 'hide','',0, {'display':'block'},{'display':'block'},"asdfiunrf98141n34ij134n09"

""" 
    if n_clicks !=None:
            else:
        return 'hide','', 0, {'display':'none'},{'display':'none'},"asdfiunrf98141n34ij134n09"
"""

@dash.callback(
    Output("number-verify-notify",'action' ),
    Output("number-verify-notify",'message'),
    Input('participant-1-phone-number','value'),
    Input('participant-2-phone-number','value'),
    prevent_initail_call = True
)
def check_phone_number(num1,num2):
    if  num1 != None and len(num1) == 10:
        response = requests.get(f"https://ai4bdmuserver.centralindia.cloudapp.azure.com/misc/findUser/{num1}")
        res = response.text
        if res == 'NO':
            return 'show',f'{num1} does not exist in Database'
    if  num2 != None and len(num2) == 10:
        response = requests.get(f"https://ai4bdmuserver.centralindia.cloudapp.azure.com/misc/findUser/{num2}")
        res = response.text
        if res == 'NO':
            return 'show',f'{num2} does not exist in Database'
    return 'hide', ''



@dash.callback(Output("player_container", "children"), Input("call-button", "n_clicks"),
background=True,)
def fetch_audio(value):
    print("inside fetch audio")
    return []
    if value is None:
        return
    else:
        sid = request.args.get('callSid')
        url = "https://kpi.knowlarity.com/Basic/v1/account/call/get-detailed-call-log?uuid="+sid
        headers = {
        'Authorization': KN_AUTH,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': KN_API_KEY,
        }
        response_post = requests.request("GET", url, headers=headers).json()
        # return response_post
        response = {}
        response['Call'] = {'Status':'incomplete'}
        # print(response_post['message'])
        if response_post.get('hangup_cause',0) == 900:
            response['Call']['Status'] = 'completed'
            if not os.path.exists(f"{ivrs_path}/{sid}.wav"):
                response_wav = requests.get(f'http://www.smartivr.in/sounds/voicemail/download/{sid}')
                with open(f"{ivrs_path}/{sid}.wav",'wb') as writer:
                    writer.write(response_wav.content)
            upload_to_azure(f'{sid}.wav')
            # Share bytes
            response['Call']['AzureUrl'] = f'https://ai4bdmustorage.blob.core.windows.net/role-play-convs/{sid}.wav?sp=r&st=2023-03-26T19:26:54Z&se=2024-06-01T03:26:54Z&spr=https&sv=2021-12-02&sr=c&sig=wp74Z7pg%2Fq3GYVXZzIMhXjnC3dwNnORTu1gj0YYDZ88%3D'
        return response
    
    print('Entered show_state',value)
    a = html.Audio(id = 'player',src='data:audio/mpeg;base64,{}'.format(base64.b64encode(open('./Shakira_-_Whenever_Wherever_(ColdMP3.com).mp3', 'rb').read()).decode()), controls = True, autoPlay = False, style = {"width":"100%"})
    print("a done")
    #return
    return a


@dash.callback(
    Output('participant-1-role-dropdown','data'),
    Output('roleplay-sub-category-dropdown','style'),
    Output('roleplay-sub-category-dropdown','data'),
    Output('state-district-dropdown','style'),
    Output('state-dropdown','data'),
    Input('roleplay-category-dropdown','value'),
    Input('roleplay-sub-category-dropdown','value'),
    Input('district-dropdown','value'),
    State('state-dropdown','value'),

    prevent_initial_update = True
    )
def get_category(value, sub_category, district, state):
    print("inside get_category")
    if value == "General":
        print("Inside General")
        
        subset = df[(df.typer == value.lower()) ]
        res = subset['role1'].unique().tolist()
        res.extend(subset['role2'].unique().tolist())
        print(res)
        return res, {'display':'none'},[],{'display':'none'},[]
    elif value == 'State':
        if sub_category != None:
            subset = df[(df['name'] == sub_category)]
            res = subset['role1'].unique().tolist()
            res.extend(subset['role2'].unique().tolist())
            print(res)
            return res, {'display':'block'} ,df[df.typer == 'state']['name'].unique().tolist(),{'display':'none'},[]


        print("Inside State")
        return[], {'display':'block'} ,df[df.typer == 'state']['name'].unique().tolist(),{'display':'none'},[]
    elif value == 'District':
        res = []
        if state != None and district != None:
            print("Inside state not none and disrict not none")
            subset = df[(df['typer'] == value.lower()) & (df['name'] == district)]
            print(subset.head())
            res = subset['role1'].unique().tolist()
            res.extend(subset['role2'].unique().tolist())
        return res, {'display':'none'},[],{'display':'block'} ,df[df.typer == 'state']['name'].unique().tolist()
    else:
        return [], {},[],{},[]

    """
    if district != None and state != None and value != None and sub_category == 'None':
        print("district and sub_category and distict, state")
        subset = df[df.typer == value.lower()]['role1'].unique().tolist()
        return subset, {'display':'none'},[],{},[]

    print(value)
    if value != None and sub_category != None:
        print("Inside final")
        subset = df[(df.typer == value.lower()) & (df['name'] == sub_category)]
        res = subset['role1'].unique().tolist()
        res.extend(subset['role2'].unique().tolist())
        print(res)
        return res,{},df[df['typer'] == value.lower()]['name'].unique().tolist(), {'display':'none'},[]

    if value != None:
        if value != 'General':
            print("value not general")
            if value  == 'District':
                print("inside disrict")
                return [],{'display':'none'},[],{'display':'block'} ,df[df.typer == 'state']['name'].unique().tolist()
            print('not general')
            res = df[df['typer'] == value.lower()]['name'].unique().tolist()

            return [],{'display':'block'}, res, {'display':'none'}, []
        subset = df[df.typer == value.lower()]['role1'].unique().tolist()
        #print(subset)
        return subset, {'display':'none'}, ["d"],{'display':'none'},[]
    return [],{},[], {},[]
    """
"""
@dash.callback(
    Output('participant-1-role-dropdown','data'),
    Input('roleplay-sub-category-dropdown','value'),
    prevent_initial_update = True
)
def get_role_1( r_category):
    print("get_role_1") 
    if r_category == "General":
        print("get roleses for general")
        subset = df[(df.typer == r_category.lower()) & (df['name'] == 'General')]

        res = subset['role1'].unique().tolist()
        res.extend(subset['role2'].unique().tolist())
        return [res]


    elif r_category == "State":
        if sub_cat != None:
            print("get roles for state",sub_cat)
            subset = df[(df['name'] == sub_cat)]
            res = subset['role1'].unique().tolist()
            res.extend(subset['role2'].unique().tolist())
            print(res)
            return res
    elif r_category == 'District':
        if state != None and district != None:
            print("get roles for district", district)
            subset = df[(df.typer == "district") & (df['name'] == district)]
            res = subset['role1'].unique().tolist()
            res.extend(subset['role2'].unique().tolist())
            return res
    else:
        return []

    """
@dash.callback(
    Output ('district-dropdown','data'),
    Input('state-dropdown','value'),
    prevent_initial_update = True
)
def get_district(state):
    return df[df.typer=='district']['name'].unique().tolist()

@dash.callback(
    Output('participant-2-role-dropdown','data'),
    Input('participant-1-role-dropdown','value'),
    State('roleplay-category-dropdown','value'),
    State('roleplay-sub-category-dropdown','value'),
    State('district-dropdown','value'),
    prevent_initial_update = True

)
def get_role_2(role1, role_category, role_sub_category, district):
    
    if role1 != None:
        if role_sub_category == None and district != None:
            role_sub_category = district
        if role_sub_category == None:
            print('inside role subset')
            subset = df[(df.typer == role_category.lower()) & (df.role1 == role1) ]['role2'].unique().tolist()
            if len(subset) == 0:
                subset = df[(df.typer == role_category.lower()) & (df.role2 == role1)]['role1'].unique().tolist()
            #print(subset)
            return subset

        subset = df[(df.typer == role_category.lower()) & (df.role1 == role1) & (df.name ==  role_sub_category)]['role2'].unique().tolist()
        if len(subset) == 0:
            subset = df[(df.typer == role_category.lower()) & (df.name ==  role_sub_category)& (df.role2 == role1)]['role1'].unique().tolist()
        #print(subset)
        return subset
    return []

@dash.callback(
    Output('topic-dropdown','data'),
    Input('participant-2-role-dropdown','value'),
    State('roleplay-category-dropdown','value'),
    State('roleplay-sub-category-dropdown','value'),
    State('participant-1-role-dropdown','value'),
    State('district-dropdown','value'),
    prevent_initial_update = True
)
def get_topic(role2, r_category, r_sub_category, role1, district):
    tocs = []
    if role2 !=None:
        if r_sub_category == None and district != None:
            r_sub_category = district
        if r_sub_category == None:
            return list(set(df[df.typer.isin([r_category.lower()])  & (df.role1.isin([role1]) | df.role2.isin([role1])) & (df.role2.isin([role2]) | df.role1.isin([role2]))]['toc'].to_list()))
        #res = df[(df.typer == r_category.lower()) & (df.role1 == role1) & (df['name'] == r_sub_category) & (df.role2 == role2)]['toc'].unique().tolist()
        tocs = list(set(df[df.typer.isin([r_category.lower()]) & df.name.isin([r_sub_category]) & (df.role1.isin([role1]) | df.role2.isin([role1])) & (df.role2.isin([role2]) | df.role1.isin([role2]))]['toc'].to_list()))
        #print(tocs)
    return tocs




if __name__ == '__main__':
    app.run_server(debug=True)

