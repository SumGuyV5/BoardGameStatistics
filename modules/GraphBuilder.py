from bokeh.models import ColumnDataSource
from bokeh.models import LabelSet
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components
import operator
import bokeh


def build_graph(feature_name, players_info):
    # ['Win Percentage', 'H-Index', 'Total Games Played', 'Wins', 'Loss', 'Total Points', 'Points Per Game']
    attr = 'win_percentage'
    if feature_name == 'Win Percentage':
        attr = 'win_percentage'
    elif feature_name == 'H-Index':
        attr = 'h_index'
    elif feature_name == 'Total Games Played':
        attr = 'total_games'
    elif feature_name == 'Wins':
        attr = 'win_count'
    elif feature_name == 'Loss':
        attr = 'loss_count'
    elif feature_name == 'Total Points':
        attr = 'points'
    elif feature_name == 'Points Per Game':
        attr = 'points_per_game'

    title = f'Players {feature_name}'
    players_info = sorted(players_info, key=operator.attrgetter(attr), reverse=True)
    players = []
    counts = []
    heights_num = 0

    for player_info in players_info:
        players.append(player_info.name)
        value = round(float(player_info.__getattribute__(attr)), 2)
        if value > heights_num:
            heights_num = value
        counts.append(value)

    source = ColumnDataSource(data=dict(players=players, counts=counts))

    p = figure(x_range=players, toolbar_location=None, title=title, plot_width=800, plot_height=700,
               tools="save")
    p.vbar(x='players', top='counts', width=0.4, source=source, legend='players', line_color='white',
           fill_color=factor_cmap('players', palette=bokeh.palettes.Category20[20], factors=players))

    labels = LabelSet(x='players', y='counts', text='counts', level='glyph', x_offset=-13.5, y_offset=0, source=source,
                      render_mode='canvas')

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    # p.y_range.end = heights_num + (100 * 0.20)
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    legend = p.legend[0]

    p.add_layout(labels)
    p.add_layout(legend, "right")

    return components(p)
