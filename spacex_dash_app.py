# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash import Input, Output
import plotly.express as px


# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # =========================================================
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    # =========================================================

    dcc.Dropdown(
        id='site-dropdown',

        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],

        value='ALL',

        placeholder='Select a Launch Site here',

        searchable=True
    ),

    html.Br(),


    # =========================================================
    # TASK 2:
    # Add a pie chart to show total successful launches
    # =========================================================

    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),


    # =========================================================
    # TASK 3: Add a slider to select payload range
    # =========================================================

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',

        min=0,
        max=10000,
        step=1000,

        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },

        value=[
            min_payload,
            max_payload
        ]
    ),


    # =========================================================
    # TASK 4:
    # Add scatter chart to show correlation between
    # payload and launch success
    # =========================================================

    html.Div(
        dcc.Graph(
            id='success-payload-scatter-chart'
        )
    )

])


# =============================================================
# TASK 2:
# Callback for site-dropdown -> success-pie-chart
# =============================================================

@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),

    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(entered_site):

    # If ALL launch sites are selected
    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site'
        )

        return fig

    # If a specific launch site is selected
    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title='Total Success Launches for Site {}'.format(
                entered_site
            )
        )

        return fig


# =============================================================
# TASK 4:
# Callback for site-dropdown + payload-slider
# -> success-payload-scatter-chart
# =============================================================

@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),

    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),

        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)
def get_scatter_plot(entered_site, payload_range):

    # Get selected payload range
    low_payload = payload_range[0]
    high_payload = payload_range[1]

    # Filter dataframe based on payload range
    filtered_df = spacex_df[
        (
            spacex_df['Payload Mass (kg)'] >= low_payload
        )
        &
        (
            spacex_df['Payload Mass (kg)'] <= high_payload
        )
    ]

    # If ALL launch sites are selected
    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,

            x='Payload Mass (kg)',

            y='class',

            color='Booster Version Category',

            title='Correlation between Payload and Success for All Sites'
        )

        return fig

    # If a specific launch site is selected
    else:

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            filtered_df,

            x='Payload Mass (kg)',

            y='class',

            color='Booster Version Category',

            title='Correlation between Payload and Success for Site {}'.format(
                entered_site
            )
        )

        return fig


# =============================================================
# Run the app
# =============================================================

if __name__ == '__main__':
    app.run(debug=True)