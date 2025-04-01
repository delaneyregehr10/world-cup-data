import dash
from dash import Dash, html, dcc, callback, Output, Input
from dash.dependencies import State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

world_cup = pd.read_csv('world_cup.csv')

world_cup['Winners'] = world_cup['Winners'].replace(to_replace = "England", value = "UK (England)")
world_cup_winners = world_cup['Winners'].unique()

world_cup_participants = pd.concat([world_cup['Winners'], world_cup['Runners_Up']]).unique()
wins = {participant: 0 for participant in world_cup_participants}
for winner in world_cup['Winners']:
    wins[winner] += 1
wins_by_country_df = pd.DataFrame(list(wins.items()), columns=['Participant', 'Wins'])

world_cup_years = world_cup['Year'].unique()
slider_marks = {int(year): str(year) for year in world_cup_years}

winners_fig = px.choropleth(
    world_cup,
    locations = world_cup_winners,
    locationmode ='country names',
    color = world_cup_winners,
    hover_name = world_cup_winners
)

wins_by_country_fig = px.choropleth(
    wins_by_country_df,
    locations = 'Participant',
    locationmode ='country names',
    color = 'Wins'
)

winner_and_runner_up_fig = px.choropleth(
    world_cup,
)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('World Cup Data'),
    html.Hr(),
    html.H3('Countries that have Won a World Cup'),
    dcc.Graph(figure = winners_fig),
    html.Hr(),
    html.H3('Number of World Cup Wins by Country'),
    dcc.Graph(figure = wins_by_country_fig),
    html.Hr(),
    html.H3('Winner & Runner-Up By Year'),

    html.Div([
        html.H4('Select Year'),
        dcc.Slider(
            id = 'world-cup-year',
            min = min(world_cup_years),        
            max = max(world_cup_years),       
            marks = slider_marks,                   
            value = 1930,                 
            step = None
        )
    ]),
    
    dcc.Graph(id='winner-and-runner-up-map')
])

@app.callback(
    dash.dependencies.Output('winner-and-runner-up-map', 'figure'),
    [dash.dependencies.Input('world-cup-year', 'value')]
)

def update_map(selected_year):
    filtered_by_year_data = world_cup[world_cup['Year'] == selected_year]
    by_year_data = pd.DataFrame({
        'Result': ['Winner', 'Runner-Up'],
        'Participant': [filtered_by_year_data['Winners'].values[0], filtered_by_year_data['Runners_Up'].values[0]],
    })

    winner_and_runner_up_fig = px.choropleth(
        by_year_data,
        locations='Participant',
        locationmode='country names',
        color='Result', 
        hover_name='Participant',
        color_discrete_map={'Winner': 'blue', 'Runner-Up': 'yellow'},
        title=f'World Cup Winner and Runner-Up for {selected_year}'
    )
    return winner_and_runner_up_fig



if __name__ == '__main__':
    app.run(debug = True)