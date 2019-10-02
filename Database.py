from flask_sqlalchemy import SQLAlchemy
import app

db_user = 'BoardGameStat'
db_password = 'B0@rdG@m39'
db_url = 'localhost'
db_name = 'BoardGameStat'

app.app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}'

db = SQLAlchemy(app.app)


def rebuild_database():
    db.drop_all()
    db.create_all()


playerdatasets = db.Table('player_datasets',
                          db.Column('player_dataset_id', db.Integer, db.ForeignKey('player_dataset.id'),
                                    primary_key=True),
                          db.Column('players_play_dataset_id', db.Integer, db.ForeignKey('players_play_dataset.id'),
                                    primary_key=True)
                          )


class PlayersPlayDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    playerdatasets = db.relationship('PlayerDataset', secondary=playerdatasets, lazy='subquery',
                                     backref=db.backref('players_play_datasets', lazy=True))
    gamedataset = db.relationship('GameDataset', backref='players_play_dataset', lazy=True)
    startposition = db.Column(db.Integer)
    colour = db.Column(db.String(40))
    score = db.Column(db.String(40))
    new = db.Column(db.Boolean)
    rating = db.Column(db.String(40))
    won = db.Column(db.Boolean)


class PlayerDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(120))
    userid = db.Column(db.Integer)
    name = db.Column(db.String(120))


class PlayDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    length = db.Column(db.Integer)
    incomplete = db.Column(db.Boolean)
    nowinstats = db.Column(db.Boolean)
    location = db.Column(db.String(120))


class GameDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(120))
    objectid = db.Column(db.Integer, unique=True)
    playersplay_id = db.Column(db.Integer, db.ForeignKey('players_play_dataset.id'), nullable=False)

