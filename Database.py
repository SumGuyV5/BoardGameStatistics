import operator
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
        rtn.append(data.plays_xml_dataset())
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

    def plays_xml_dataset(self):
        plays = PlaysXMLDataset(id=self.id, date=self.date, quantity=self.quantity, length=self.length,
                                incomplete=self.incomplete, nowinstats=self.nowinstats, location=self.location,
                                game_name=self.gamedataset.name, gameid=self.gamedataset.id)

        for x in self.playersplaydataset:
            plays.players.append(x.player_xml_dataset())

        return plays


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

    def player_xml_dataset(self):
        return PlayerXMLDataset(username=self.playerdataset.username, userid=self.playerdataset.userid,
                                name=self.playerdataset.name, startposition=self.startposition, colour=self.colour,
                                score=self.score, new=self.new, rating=self.rating, won=self.won)
