from bokeh.models import ColumnDataSource
from bokeh.models import LabelSet
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components
import bokeh

ignore = ['Keith', 'Paul', 'Dempsey', 'Other', 'Kelly', 'Alyssa', 'Player 6', 'Mark', 'Player 7',
          'Beulah', 'Besa', 'Player 5', 'Raymon', 'Play 2', 'Jay', 'Play 6', 'Play 5', 'Play 4', 'Play 3',
          'Anthony', 'Bill']


def build_graph(feature_name):
    from DatabaseProcessing import win_percentage, h_index, total_games, win_count, loss_count, total_points, \
        points_per_game
    # ['Win Percentage', 'H-Index', 'Total Games Played', 'Wins', 'Loss', 'Total Points', 'Points Per Game']
    players_info = {}
    if feature_name == 'Win Percentage':
        players_info = win_percentage()
    if feature_name == 'H-Index':
        players_info = h_index()
    elif feature_name == 'Total Games Played':
        players_info = total_games()
    elif feature_name == 'Wins':
        players_info = win_count()
    elif feature_name == 'Loss':
        players_info = loss_count()
    elif feature_name == 'Total Points':
        players_info = total_points()
    elif feature_name == 'Points Per Game':
        players_info = points_per_game()

    title = f'Players {feature_name}'

    players = []
    counts = []
    heights_num = 0

    for key, value in sorted(players_info.items(), key=lambda item: (item[1], item[0]), reverse=True):
        players.append(key)
        value = round(float(value), 2)
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
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    legend = p.legend[0]

    p.add_layout(labels)
    p.add_layout(legend, "right")

    return components(p)
