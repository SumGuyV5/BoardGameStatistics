from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from modules.GraphBuilder import build_graph, build_graph2
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

@app.route('/test')
def test():
    current_feature_name = request.args.get("feature_name")
    if current_feature_name is None:
        current_feature_name = feature_names[0]

    script, div = build_graph2(current_feature_name)

    return render_template('index.html', script=script, div=div, feature_names=feature_names,
                           current_feature_name=current_feature_name)


@app.route('/fullxmldownload')
def fullxmldownload():
    player_data.force_refresh()
    return render_template('index.html')


@app.route('/fullflush')
def fullflush():
    """
    fully deletes the database and rereads the xml files and enters them into the database
    :return:
    """
    from DatabaseInteractions import rebuild_database, load_xml_into_database
    rebuild_database()

    load_xml_into_database(player_data.read_all())
    return render_template('index.html')


@app.route('/update')
def update():
    return render_template('index.html')


@app.route('/')
def index():

    from DatabaseInteractions import load_database_into_xml
    current_feature_name = request.args.get("feature_name")
    if current_feature_name is None:
        current_feature_name = feature_names[0]

    script, div = build_graph(current_feature_name, player_data.read(load_database_into_xml()))

    return render_template('index.html', script=script, div=div, feature_names=feature_names,
                           current_feature_name=current_feature_name)


if __name__ == '__main__':
    app.run()
