import dash
from dash import html
import os


layout = html.Div(children=[
                html.I(className="bi bi-book home-book"),
                html.H1("Restaurant Name"),
                html.H3("Booking Manager")
            ],
            className="home-body"
)

dash.register_page(os.path.basename(__file__), name='Home', path="/", layout=layout)
