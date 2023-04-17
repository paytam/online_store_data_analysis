import dash_bootstrap_components as dbc
import pandas as pd
from utilities.pandas_helper import PandasHelper
from dash import (
    Input,
    Output,
    State,
    callback,
    dash_table,
    dcc,
    html,
    no_update,
    register_page,
    ctx,
)
from dash.exceptions import PreventUpdate
from typing import List, Dict

# CONSTANTS section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
register_page(__name__, name="Products", order=3)

# load ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pandas_helper: PandasHelper = PandasHelper(file_path="../../dataset/merged_data.csv")

# html ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# my Selectors ---------------------------------
mySelectors = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    id="product_label_class",
                                    children="Class:",
                                    className="",
                                ),
                                dcc.Dropdown(
                                    pandas_helper.df["Description"].unique(),
                                    id="product_Class",
                                    multi=True,
                                ),
                            ],
                            className="mb-4",
                        ),
                    ],
                    className="cPlatyDir2",
                ),
            ],
            className="",
        )
    ],
    className="col-12 col-lg-3 mb-1 mt-4",
    id="product_cross-filter-options",
)

# main Div ----------------------------------
layout = html.Div(
    [
        dcc.Location(id="product_url", refresh=True),
        dcc.Store(id="session", storage_type="session"),
        mySelectors,
        html.Div(
            [
                html.Div(
                    id="cards",
                    children=[],
                    className="row mx-0 mt-4",
                ),
                html.Div(
                    [
                        dbc.Spinner(
                            id="product_loading-1",
                            children=[
                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            data=pandas_helper.df.head(100).to_dict(
                                                "records"
                                            ),
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in pandas_helper.df.columns
                                            ],
                                            id="product_table_result_1",
                                            # row_selectable="single",
                                            page_size=50,
                                            page_current=0,
                                            filter_action="custom",
                                            filter_query="",
                                            sort_action="custom",
                                            sort_mode="multi",
                                            sort_by=[],
                                            fixed_rows={"headers": True},
                                            style_table={
                                                "maxHeight": "313px",
                                            },
                                            style_cell={
                                                "minWidth": "120px",
                                                "width": "120px",
                                                "maxWidth": "120px",
                                                "overflow": "hidden",
                                                "textOverflow": "ellipsis",
                                                "whiteSpase": "nowrap",
                                            },
                                        )
                                    ]
                                )
                            ],
                            color="primary",
                        )
                    ],
                    className="col-12 mt-4",
                ),
            ],
            className="col-12 col-lg-9 ps-0 pb-4",
        ),
    ],
    id="product_mainContainer",
    className="row",
)


# callbacks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@callback(
    Output("product_table_result_1", "data"),
    Input("product_Class", "value"),
)
def get_invoices_by_product(v):
    if v is None:
        return (no_update,)
    df = pandas_helper.df
    return (df[["Description" == v]].to_dict("records"),)
