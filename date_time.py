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
from datetime import datetime, timedelta, date

import dash_mantine_components as dmc
from dash import Input, Output, html, callback
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], background_callback_manager=background_callback_manager)

app.layout = html.Div(
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


@callback(
    Output("selected-date-date-range-picker", "children"),
    Input("date-range-picker", "value"),
)
def update_output(dates):
    prefix = "You have selected: "
    if dates:
        return prefix + "   -   ".join(dates)
    else:
        raise PreventUpdate



if __name__ == '__main__':
    app.run_server(debug=True)
