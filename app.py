from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from modules.GraphBuilder import build_graph
from modules.PlayerData import PlayerData


db_user = 'BoardGameStat'
db_password = 'B0@rdG@m39'
db_url = 'localhost'
db_name = 'BoardGameStat'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}'

db = SQLAlchemy(app)

player_data = PlayerData()

feature_names = ['Win Percentage', 'H-Index', 'Total Games Played', 'Wins', 'Loss', 'Total Points', 'Points Per Game']


@app.route('/refresh')
def refresh():
    from Database import rebuild_database, load_data_into_database
    tmp = player_data.players_info
    rebuild_database()
    load_data_into_database(player_data.readXML.plays)
    return render_template('index.html')


@app.route('/')
def index():
    from Database import load_database
    current_feature_name = request.args.get("feature_name")
    if current_feature_name is None:
        current_feature_name = feature_names[0]

    script, div = build_graph(current_feature_name, player_data.players_info)
    script, div = build_graph(current_feature_name, player_data.read(load_database()))

    return render_template('index.html', script=script, div=div, feature_names=feature_names,
                           current_feature_name=current_feature_name)


if __name__ == '__main__':
    app.run()
