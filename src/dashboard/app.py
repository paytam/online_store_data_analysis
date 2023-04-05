# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 14011211
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html, page_container, page_registry
import itertools


def create_different_themes():
    themes = [
        "CERULEAN",
        "COSMO",
        "CYBORG",
        "DARKLY",
        "FLATLY",
        "JOURNAL",
        "LITERA",
        "LUMEN",
        "LUX",
        "MATERIA",
    ]
    return dbc.DropdownMenu(
        [dbc.DropdownMenuItem(theme, id=theme) for theme in themes],
        label="Themes",
        nav=True,
        id="cmb_themes",
    )

def create_menus1():
    nav_contents = []

    for i, page in enumerate(page_registry.values()):
        if page["order"] == 0:
            nav_contents.append(
                dbc.Nav(
                    dbc.NavItem(
                        dbc.NavLink(
                            id={"type": "page", "index": i},
                            children=page["name"],
                            href=page["relative_path"],
                            active="exact",
                            n_clicks=0,
                            className="cCursorPointer cFontSize13 cFontWeight  cGpTransition   ",
                        )
                    ),
                    className="col-lg-auto col-xl-auto d-flex align-items-center px-0  borhanStyle154 ",
                )
            )
        else:
            nav_contents.append(
                dbc.Nav(
                    dbc.NavItem(
                        dbc.NavLink(
                            id={"type": "page", "index": i},
                            children=page["name"],
                            href=page["relative_path"],
                            active="exact",
                            n_clicks=0,
                            className="cCursorPointer cFontSize13 cFontWeight  cGpTransition   ",
                        )
                    ),
                    className="col-lg-auto col-xl-auto d-flex align-items-center px-0  borhanStyle155 ",
                )
            )
    return nav_contents


# Define the navbar structure
def navbar():
    layout = html.Div(
        [
            html.Div(
                [html.Div(create_menus1(), className="row ")],
                className="col-12 cZindex999 shadow-sm cPlatyNavBar1 px-4 borhanBg73 borhanStyle153",
            )
        ],
        className="row",
    )

    return layout


app: Dash = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        "",
        "",
        "",
        "",
        "",
    ],
)

server = app.server

app.layout = html.Div(
    [
        dcc.Store(id="tag_id"),
        dcc.Store(id="nothing"),
        navbar(),
        page_container,
    ],
    className="container-fluid",
)
