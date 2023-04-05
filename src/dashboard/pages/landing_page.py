from dash import (
    Dash,
    dcc,
    html,
    register_page,
    callback,
    Input,
    Output,
    State,
    ctx,
    no_update,
    clientside_callback,
    ALL,
    callback_context,
)

register_page(__name__, name="Data analysis", order=0, path="/")

markdown_text = """
# data analysis dashboard

The aim of this dashboard is depicting ...
"""

layout = html.Div(
    children=[
        dcc.Location(id="landing_url", refresh=False),
        dcc.Store(id="session", storage_type="session"),
        dcc.Markdown(markdown_text),
        html.Label(id="l"),
    ],
    id="main_div",
)


@callback(
    Output("tag_id", "data"),
    Input({"type": "page", "index": ALL}, "n_clicks"),
)
def tag_click(nav_tag):
    triggered = [t["prop_id"].replace(".n_clicks", "")
                 for t in callback_context.triggered if "n_clicks" in t["prop_id"]]
    if triggered:
        return triggered[0]
    return ""


clientside_callback(
    """
    function disableNewTabClick(tag_id) {
        var tags = document.querySelectorAll("a[class*='nav-link']");
        for(let i=0; i < tags.length; i++){
            tags[i].setAttribute("oncontextmenu","return false;");
            tags[i].href = 'javascript:void(0);';
            if (tag_id != ""){
                if (tags[i].classList.contains("active")){
                    tags[i].classList.remove("active");
                };
                document.getElementById(tag_id).classList.add("active");
            };
        };
        return ""
    } 
    """,
    Output("nothing", "data"),
    Input("tag_id", "data"),
)


@callback(
    Output("session", "data"),
    Input("landing_url", "search"),
    State("session", "data"),
)
def display_page(se, data):
    if data is None:
        data = {}
    for param in se.split("&"):
        if param == "":
            continue
        p = param.split("=")
        data[p[0].replace("?", "")] = p[1]
    return data
