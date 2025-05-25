import dash
from dash import dcc, html, Output, Input
import geopandas as gpd
import pydeck as pdk
import json
from shapely import wkt
from shapely.geometry import mapping
from geodatasets import get_path
import os

from sports_facilities.preprocess_data import preprocess_data

FOLDER = "sports_facilities"
HTML_PATH = "sports_filtered_map.html"

# Define RGBA colors
RGBA = {
    'blue': [0, 0, 255, 160], 'green': [0, 128, 0, 160], 'orange': [255, 165, 0, 160],
    'purple': [128, 0, 128, 160], 'red': [255, 0, 0, 160], 'gray': [128, 128, 128, 160],
    'pink': [255, 192, 203, 160], 'brown': [139, 69, 19, 160], 'teal': [0, 128, 128, 160],
    'gold': [255, 215, 0, 160], 'cyan': [0, 255, 255, 160], 'magenta': [255, 0, 255, 160],
    'navy': [0, 0, 128, 160], 'olive': [128, 128, 0, 160], 'tomato': [255, 99, 71, 160],
    'orchid': [218, 112, 214, 160], 'lime': [0, 255, 0, 160]
}

# Use a fixed global color map
df_all = preprocess_data(FOLDER)
df_all["PRIMARY_SPORT"] = df_all["PRIMARY_SPORT"].fillna("Unknown").astype(str)
categories_all = sorted(df_all["PRIMARY_SPORT"].unique())
color_map_global = {cat: list(RGBA.keys())[i % len(RGBA)] for i, cat in enumerate(categories_all)}

def get_rgba(sport):
    return RGBA.get(color_map_global.get(sport, 'gray'), [128, 128, 128, 160])

# generates the chloropleth map
def generate_filtered_map(selected_sport):
    df = df_all.copy()
    df["geometry"] = df["multipolygon"].map(wkt.loads).apply(lambda geom: geom.simplify(0.0001))

    if selected_sport != "All":
        df = df[df["PRIMARY_SPORT"] == selected_sport]

    df["fill_color"] = df["PRIMARY_SPORT"].map(get_rgba)

    # gets the multi polygons of each facility
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    nyc_boundary = gpd.read_file(get_path("nybb")).to_crs("EPSG:4326").union_all()
    gdf = gdf[gdf.geometry.intersects(nyc_boundary)]
    gdf["geometry"] = gdf.geometry.intersection(nyc_boundary)
    geojson_data = json.loads(gdf.to_json())

    # layer of the entire map
    geojson_layer = pdk.Layer(
        "GeoJsonLayer",
        data=geojson_data,
        filled=True,
        get_fill_color="properties.fill_color",
        get_line_color=[80, 80, 80],
        pickable=True
    )

    # defines boundary of NYC
    boundary_layer = pdk.Layer(
        "PolygonLayer",
        data=[{"polygon": mapping(nyc_boundary)["coordinates"]}],
        get_polygon="polygon",
        get_line_color=[0, 0, 0],
        get_fill_color=[0, 0, 0, 0],
        line_width_min_pixels=2,
        stroked=True,
        filled=False
    )

    # settings to adjust zoom
    view_state = pdk.ViewState(
        latitude=40.7128,
        longitude=-74.0060,
        zoom=10,
        pitch=0,
        bearing=0,
        min_zoom=5,
        max_zoom=18
    )

    # adding both map and boundary layers
    r = pdk.Deck(
        layers=[geojson_layer, boundary_layer],
        initial_view_state=view_state,
        tooltip={"text": "{SYSTEM} ({PRIMARY_SPORT})"}
    )
    r.to_html(HTML_PATH)

# Initial map to load primary sports options
available_sports = ["All"] + categories_all
generate_filtered_map("All")

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H3("NYC Sports Facility Map with Filter"),
        dcc.Dropdown(
            id="sport-dropdown",
            options=[{"label": sport, "value": sport} for sport in available_sports],
            value="All",
            style={"width": "300px"}
        )
    ], style={"position": "absolute", "top": "20px", "right": "20px", "zIndex": 1000, "backgroundColor": "white", "padding": "10px", "boxShadow": "0px 0px 5px rgba(0,0,0,0.3)"}),
    html.Iframe(id="map-frame", srcDoc=open(HTML_PATH).read(), width="100%", height="700"),

    # defines the legend
    html.Div([
        html.Details([
            html.Summary("Legend (click to expand)"),
            html.Ul([
                html.Li("Basketball (BKB)", style={"color": "blue"}),
                html.Li("Bocce (BOC)", style={"color": "green"}),
                html.Li("Baseball (BSB)", style={"color": "orange"}),
                html.Li("Cricket (CRK)", style={"color": "purple"}),
                html.Li("Football (FTB)", style={"color": "red"}),
                html.Li("Handball (HDB)", style={"color": "gray"}),
                html.Li("Hockey (HKY)", style={"color": "pink"}),
                html.Li("Multi Purpose Play (MPPA)", style={"color": "brown"}),
                html.Li("Netball (NTB)", style={"color": "teal"}),
                html.Li("Pickleball (PKB)", style={"color": "gold"}),
                html.Li("Rugby (RBY)", style={"color": "cyan"}),
                html.Li("Soccer (SCR)", style={"color": "magenta"}),
                html.Li("Softball (SFB)", style={"color": "navy"}),
                html.Li("Tennis (TNS)", style={"color": "olive"}),
                html.Li("Track (TRK)", style={"color": "tomato"}),
                html.Li("Volleyball (VLB)", style={"color": "lime"}),
                html.Li("Unknown", style={"color": "orchid"})
            ], style={"listStyleType": "none", "paddingLeft": 0})
        ])
    ], style={"position": "absolute", "bottom": "20px", "left": "20px", "zIndex": 1000, "backgroundColor": "white", "padding": "10px", "boxShadow": "0px 0px 5px rgba(0,0,0,0.3)"})
])

# updates the map in case of different filtering
@app.callback(
    Output("map-frame", "srcDoc"),
    Input("sport-dropdown", "value")
)
def update_map(sport):
    generate_filtered_map(sport)
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)
