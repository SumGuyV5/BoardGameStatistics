import time
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from modules.GraphBuilder import build_graph
from modules.PlayerData import PlayerData
from flask_heroku import Heroku
from flask_executor import Executor

db_user = 'BoardGameStat'
db_password = '04122442134234cdd2da81598665ffa1b66ec281678934c036377f7271eb0de133bd531b030d62885b7911a' \
              '5260b731f6a82d89666d4bd033552441fa650be98'
db_url = 'localhost'
db_name = 'BoardGameStat'

app = Flask(__name__)
heroku = Heroku(app)
executor = Executor(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}'

db = SQLAlchemy(app)

player_data = PlayerData()

feature_names = ['Win Percentage', 'H-Index', 'Total Games Played', 'Wins', 'Loss', 'Total Points', 'Points Per Game']
feature_database = ['Nothing', 'Download All XML Files', 'Read All XML Files', 'Inputting XML Data', 'Clear Database',
                    'Inputting and Read']


def datainstall():
    player_data.clear()
    player_data.download_all()
    player_data.read_all()
    player_data.input_data()


def gen(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route('/data')
def data():
    executor.submit(datainstall)
    return render_template('index.html')

@app.route('/database')
def database():
    current_feature_database = request.args.get("feature_database")
    if current_feature_database is None:
        current_feature_database = feature_database[0]

    rows = None
    if current_feature_database == feature_database[0]:
        rows = ["Nothing."]
    elif current_feature_database == feature_database[1]:
        rows = player_data.download_all()
    elif current_feature_database == feature_database[2]:
        rows = player_data.read_all()
    elif current_feature_database == feature_database[3]:
        rows = player_data.input_data()
    elif current_feature_database == feature_database[4]:
        rows = player_data.clear()
    elif current_feature_database == feature_database[5]:
        rows = player_data.input_read()

    return Response(gen('infodisplay.html', rows=rows, feature_database=feature_database,
                        current_feature_database=current_feature_database))


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
