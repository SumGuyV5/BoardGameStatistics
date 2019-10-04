from app import db
from BGGModule.PlaysXMLDataset import PlaysXMLDataset
from BGGModule.PlayerXMLDataset import PlayerXMLDataset


def rebuild_database():
    db.drop_all()
    db.create_all()


def load_database():
    rtn = []
    all_datas = db.session.query(PlayDataset).all()
    for data in all_datas:
        plays = PlaysXMLDataset()
        plays.id = data.id
        plays.date = data.date
        plays.quantity = data.quantity
        plays.length = data.length
        plays.incomplete = data.incomplete
        plays.nowinstats = data.nowinstats
        plays.location = data.location

        plays.game_name = data.gamedataset.name
        plays.gameid = data.gamedataset.id

        for playersplay in data.playersplaydataset:
            players = PlayerXMLDataset()
            players.username = playersplay.playerdataset.username
            players.userid = playersplay.playerdataset.userid
            players.name = playersplay.playerdataset.name
            players.startposition = playersplay.startposition
            players.colour = playersplay.colour
            players.score = playersplay.score
            players.new = playersplay.new
            players.rating = playersplay.rating
            players.won = playersplay.won
            plays.players.append(players)
        rtn.append(plays)
    return rtn


def load_data_into_database(plays):
    game_pass = {}
    player_pass = {}
    for play in plays:
        playdataset = PlayDataset(id=play.id, date=play.date, quantity=play.quantity, length=play.length,
                                  incomplete=play.incomplete, nowinstats=play.nowinstats, location=play.location)

        for player in play.players:
            if player.name not in player_pass:
                playerdataset = PlayerDataset(username=player.username, userid=player.userid, name=player.name)
                db.session.add(playerdataset)
                player_pass[player.name] = playerdataset
            playersplaydataset = PlayersPlayDataset(playerdataset=player_pass[player.name],  playdataset=playdataset,
                                                    startposition=player.startposition, colour=player.colour,
                                                    score=player.score, new=player.new, rating=player.rating,
                                                    won=player.won)
            db.session.add(playersplaydataset)

        if play.gameid not in game_pass:
            gamedataset = GameDataset(id=play.gameid, name=play.game_name)
            db.session.add(gamedataset)
            game_pass[play.gameid] = gamedataset

        playdataset.gamedataset = game_pass[play.gameid]

        db.session.add(playdataset)
        db.session.commit()


class GameDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(120))


class PlayerDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(120))
    userid = db.Column(db.Integer)
    name = db.Column(db.String(120), unique=True, nullable=False)


class PlayDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    length = db.Column(db.Integer)
    incomplete = db.Column(db.Boolean)
    nowinstats = db.Column(db.Boolean)
    location = db.Column(db.String(120))
    gamedataset_id = db.Column(db.Integer, db.ForeignKey('game_dataset.id'), nullable=False)  # One to One
    gamedataset = db.relationship('GameDataset', backref=db.backref('play_dataset', lazy=True))  # One to One
    playersplaydataset = db.relationship('PlayersPlayDataset',
                                         backref=db.backref('play_dataset', lazy=True))  # One to Many


class PlayersPlayDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    playerdataset_id = db.Column(db.Integer, db.ForeignKey('player_dataset.id'), nullable=False)  # One to One
    playerdataset = db.relationship('PlayerDataset',
                                    backref=db.backref('players_play_dataset', lazy=True))  # One to One
    playdataset_id = db.Column(db.Integer, db.ForeignKey('play_dataset.id'), nullable=False)
    playdataset = db.relationship('PlayDataset', backref=db.backref('players_play_dataset', lazy=True))  # Many to One
    startposition = db.Column(db.Integer)
    colour = db.Column(db.String(40))
    score = db.Column(db.String(40))
    new = db.Column(db.Boolean)
    rating = db.Column(db.String(40))
    won = db.Column(db.Boolean)
