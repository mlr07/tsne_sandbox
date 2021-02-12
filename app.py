import base64
import glob
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output


images = glob.glob("test_images/*")
x = np.random.randint(10, size=len(images))
y = np.random.randint(10, size=len(images))
df = pd.DataFrame({"X": x, "Y": y, "IMG": images})


def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())


app = dash.Dash()

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id="fake-tsne-plot",
            figure={
                "data": [
                    go.Scatter(
                        x=df["X"],
                        y=df["Y"],
                        dy=1,
                        mode="markers",
                        marker={
                            "size": 12,
                            "color": "green",
                            "line": {"width": 2 }
                        }
                    )
                ],
                "layout": go.Layout(
                    title="Fake TSNE Image Plot",
                    hovermode="closest"
                )
            }
        )
    ], style={"width": "60%", "float": "left"}),

    html.Div([
        html.H3("JSON pointIndex connects data to plot"),
        html.Pre(id='hover-data', style={'paddingTop': 35})
    ], style={'width': '30%'}),

    html.Div([
        html.H3("Image accessed by index from data"),
        html.Img(id="hover-image", src="children", height=300)
    ], style={"width": "30%"})
])


@app.callback(
    Output('hover-data', 'children'),
    [Input('fake-tsne-plot', 'hoverData')])
def callback_image(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output("hover-image", "src"),
    [Input("fake-tsne-plot", "hoverData")]
)
def callback_show_image(hoverData):
    idx = hoverData["points"][0]["pointIndex"]

    # get path
    path = df.iloc[idx]["IMG"]

    return encode_image(path)


if __name__ == "__main__":
    app.run_server(debug=True)
