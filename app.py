from flask import Flask, render_template, request
from modules.GraphBuilder import build_graph
from modules.PlayerData import PlayerData

app = Flask(__name__)

player_data = PlayerData()

feature_names = ['Win Percentage', 'H-Index', 'Total Games Played', 'Wins', 'Loss', 'Total Points', 'Points Per Game']


@app.route('/refresh')
def refresh():
    player_data.force_refresh()
    return render_template('index.html')


@app.route('/')
def index():
    current_feature_name = request.args.get("feature_name")
    if current_feature_name is None:
        current_feature_name = "Win Percentage"

    script, div = build_graph(current_feature_name, player_data.players_info)
    return render_template('index.html', script=script, div=div, feature_names=feature_names,
                           current_feature_name=current_feature_name)


if __name__ == '__main__':
    app.run()
