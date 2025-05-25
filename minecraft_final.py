import dash
import dash_cytoscape as cyto
from dash import html
import pandas as pd
import os
import ast
import re
from dash import Input, Output, State, callback_context

ITEM_KEYS = {"WoodenPlank": ['OakPlanks']}


cyto.load_extra_layouts()

FOLDER = "minecraft"

def process_network():

    # reads the minecraft_ingredients excel sheet
    minecraft_recipes = pd.read_excel(os.path.join(FOLDER, 'minecraft_recipes.xlsx'))

    nodes = []
    edges = []
    existing_nodes = []

    for index, row in minecraft_recipes.iterrows():
        ingredients = []

        name = row["Name"]
        name_key = "".join(name.split())

        node = {
            "data": {
                "id": name_key,
                "label": name,
                "description": row["Description"].strip(),
                "recipe": row["Image"].strip(),
                "category": row["Category"]  # ✅ add this line
            }
        }
        nodes.append(node)
        existing_nodes.append(name_key)

        if " & " in row["Ingredients"] and " or " in row["Ingredients"]:
            ingredients = []
            sub_ingredients = row["Ingredients"].split(" & ")
            for sub in sub_ingredients:
                sub = sub.split(" or ")
                ingredients.extend(sub)

        elif " & " in row["Ingredients"]:
            ingredients = row["Ingredients"].split(" & ")
        elif " or " in row["Ingredients"]:
            ingredients = row["Ingredients"].split(" or ")
        else:
            ingredients = [row["Ingredients"]]

        for ingredient in ingredients:
            ingredient_key = "".join(ingredient.split())
            if ingredient_key not in existing_nodes:
                node = {
                    "data": {
                        "id": ingredient_key,
                        "label": ingredient,
                        "category": "Ingredient"  # ✅ or a proper category if known
                    }
                }
                nodes.append(node)
                existing_nodes.append(ingredient_key)

    # iterates through the dataframe again to get the edges
    for index, row in minecraft_recipes.iterrows():

        name_key = "".join(row["Name"].split())

        # cleans the ingredients
        if " & " in row["Ingredients"] and " or " in row["Ingredients"]:
            ingredients = []
            sub_ingredients = row["Ingredients"].split(" & ")
            for sub in sub_ingredients:
                sub = sub.split(" or ")
                ingredients.extend(sub)

        elif " & " in row["Ingredients"]:
            ingredients = row["Ingredients"].split(" & ")
        elif " or " in row["Ingredients"]:
            ingredients = row["Ingredients"].split(" or ")
        else:
            ingredients = [row["Ingredients"]]

        # iterates through each ingredient
        for ingredient in ingredients:
            ingredient_key = "".join(ingredient.split())
            edge = {"data": {"source": ingredient_key, "target": name_key}}
            edges.append(edge)
        
    elements = nodes + edges
        
    return elements

def category_color_map(color_map):
    selectors = []

    for category in color_map:
        selector = {
            "selector": f'[category = "{category}"]',
            "style": {
                "background-color": f"{color_map[category]}"
            }
        }
        selectors.append(selector)

    return selectors

def create_app():
    elements = process_network()
    global cached_elements
    cached_elements = elements  # ✅ store for reset

    # defines mapping of colors
    CATEGORY_COLORS = {
        "Basic Recipes": "#FFB347",      # Orange
        "Block Recipes": "#87CEEB",      # Sky Blue
        "Tool Recipes": "#A569BD",       # Purple
        "Defence Recipes": "#FF6F61",    # Coral Red
        "Mechanism Recipes": "#5DADE2",  # Light Blue
        "Food Recipes": "#F4D03F",       # Yellow
        "Other Recipes": "#95A5A6",      # Gray
        "Dye Recipes": "#E67E22",        # Burnt Orange
        "Wool Recipes": "#EC7063",       # Light Red
        "Brewing Recipes": "#58D68D",    # Light Green
        "Ingredient": "#B0B0B0"
    }

    category_styles = category_color_map(CATEGORY_COLORS)
    # print(category_styles)
    # exit()

    basic_styles = [
        {
            'selector': 'node',
            'style': {
                #'background-color': 'mapData(category, "Basic Recipes", "#FFB347", "Block Recipes", "#87CEEB", "Tool Recipes", "#A569BD", "Defence Recipes", "#FF6F61", "Mechanism Recipes", "#5DADE2", "Food Recipes", "#F4D03F", "Other Recipes", "#95A5A6", "Dye Recipes", "#E67E22", "Wool Recipes", "#EC7063", "Brewing Recipes", "#58D68D", "Ingredient", "#B0B0B0")',
                'label': 'data(label)',
                'width': 80,
                'height': 80,
                'font-size': 16,
                'text-valign': 'center',
                'text-halign': 'center',
                'color': 'black',
                'text-wrap': 'wrap',
                'text-max-width': 80,
            }
        },
        {
            'selector': 'edge',
            'style': {
                'line-color': '#7FDBFF',
                'target-arrow-color': '#7FDBFF',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'width': 2,
            }
        }
    ]

    # makes the stylesheet
    stylesheet = basic_styles + category_styles
    

    app = dash.Dash(__name__)

    app.layout = html.Div([
    html.H1("Minecraft Crafting Network", style={'textAlign': 'center'}),
    html.Button("Reset View", id="reset-button", n_clicks=0, style={"margin": "10px"}),

    # 👇 Flex container for graph + side panel
    html.Div([
        # Graph
        cyto.Cytoscape(
            id='network-graph',
            elements=elements,
            layout={
                'name': 'cose-bilkent',
                'idealEdgeLength': 250,
                'nodeRepulsion': 15000,
                'gravity': 0.15,
                'numIter': 4000,
                'tile': True,
            },
            style={'width': '70%', 'height': '800px'},
            minZoom=0.1,
            maxZoom=2.0,
            userZoomingEnabled=True,
            userPanningEnabled=True,
            stylesheet=stylesheet
        ),

        # Side panel
        html.Div(id='node-info', style={
            'width': '30%',
            'height': '800px',
            'padding': '20px',
            'borderLeft': '2px solid #ccc',
            'overflowY': 'auto',
            'boxSizing': 'border-box'
        })
    ], style={  # 👈 Flex container style
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-between'
    })
])


    @app.callback(
        Output('network-graph', 'elements'),
        Input('network-graph', 'tapNodeData'),
        State('network-graph', 'elements'),
        prevent_initial_call=True
    )
    def filter_neighbors(clicked_node, all_elements):
        if not clicked_node:
            return all_elements

        node_id = clicked_node['id']
        neighbors = set()
        filtered_nodes = []
        filtered_edges = []

        for el in all_elements:
            if 'source' in el['data'] and 'target' in el['data']:
                if el['data']['source'] == node_id or el['data']['target'] == node_id:
                    filtered_edges.append(el)
                    neighbors.add(el['data']['source'])
                    neighbors.add(el['data']['target'])

        for el in all_elements:
            if 'id' in el['data'] and el['data']['id'] in neighbors:
                filtered_nodes.append(el)

        return filtered_nodes + filtered_edges

    @app.callback(
        Output('network-graph', 'elements', allow_duplicate=True),
        Input('reset-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_view(n):
        return cached_elements

    @app.callback(
        Output('node-info', 'children', allow_duplicate=True),
        Input('network-graph', 'tapNodeData'),
        prevent_initial_call=True
    )
    def show_node_info(node):
        if not node:
            return ""

        return html.Div([
            html.H3(node.get('label', '')),
            html.Img(src=node.get('recipe', ''), style={'width': '100%', 'marginBottom': '20px'}) if node.get('recipe') else None,
            html.P(f"Description: {node.get('description', 'No description available.')}"),
        ])

    return app



# Run app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)