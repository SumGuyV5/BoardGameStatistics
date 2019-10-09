import time
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from modules.GraphBuilder import build_graph
from modules.PlayerData import PlayerData
from flask_heroku import Heroku

db_user = 'BoardGameStat'
db_password = '04122442134234cdd2da81598665ffa1b66ec281678934c036377f7271eb0de133bd531b030d62885b7911a' \
              '5260b731f6a82d89666d4bd033552441fa650be98'
db_url = 'localhost'
db_name = 'BoardGameStat'

app = Flask(__name__)
heroku = Heroku(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}'

db = SQLAlchemy(app)

player_data = PlayerData()

feature_names = ['Win Percentage', 'H-Index', 'Total Games Played', 'Wins', 'Loss', 'Total Points', 'Points Per Game']


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
    from DatabaseInteractions import number_records
    player_data.update(number_records())
    return render_template('index.html')


@app.route('/')
def index():
    current_feature_name = request.args.get("feature_name")
    if current_feature_name is None:
        current_feature_name = feature_names[0]

    start_time = time.time()
    script, div = build_graph(current_feature_name)
    print(f"{current_feature_name} took. {time.time() - start_time} to run")

    return render_template('index.html', script=script, div=div, feature_names=feature_names,
                           current_feature_name=current_feature_name)


if __name__ == '__main__':
    app.run()
