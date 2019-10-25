from app import db
from BGGModule.PlaysXMLDataset import PlaysXMLDataset
from BGGModule.PlayerXMLDataset import PlayerXMLDataset


class GameDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(120))

    @property
    def xml(self):
        return PlaysXMLDataset(id=self.id, game_name=self.name)

    @xml.setter
    def xml(self, val):
        self.name = val.game_name
        self.id = val.gameid


class PlayerDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(120))
    userid = db.Column(db.Integer)
    name = db.Column(db.String(120), unique=True, nullable=False)

    @property
    def xml(self):
        return PlayerXMLDataset(username=self.username, userid=self.userid, name=self.name)

    @xml.setter
    def xml(self, val):
        self.username = val.username
        self.userid = val.userid
        self.name = val.name


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

    @property
    def xml(self):
        plays = PlaysXMLDataset(id=self.id, date=self.date, quantity=self.quantity, length=self.length,
                                incomplete=self.incomplete, nowinstats=self.nowinstats, location=self.location,
                                game_name=self.gamedataset.name, gameid=self.gamedataset.id)

        for x in self.playersplaydataset:
            plays.players.append(x.xml)

        return plays

    @xml.setter
    def xml(self, val):
        self.id = val.id
        self.date = val.date
        self.quantity = val.quantity
        self.length = val.length
        self.incomplete = val.incomplete
        self.nowinstats = val.nowinstats
        self.location = val.location
        self.gamedataset = GameDataset.query.filter_by(id=val.gameid).first()
        if self.gamedataset is None:
            self.gamedataset = GameDataset(xml=val)
        for player in val.players:
            self.playersplaydataset.append(PlayersPlayDataset(xml=player))


class PlayersPlayDataset(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    playerdataset_id = db.Column(db.Integer, db.ForeignKey('player_dataset.id'), nullable=False)  # One to One
    playerdataset = db.relationship('PlayerDataset',
                                    backref=db.backref('players_play_dataset', lazy=True))  # One to One
    playdataset_id = db.Column(db.Integer, db.ForeignKey('play_dataset.id'), nullable=False)
    playdataset = db.relationship('PlayDataset', backref=db.backref('players_play_dataset', lazy=True))  # Many to One
    position = db.Column(db.Integer)
    colour = db.Column(db.String(40))
    score = db.Column(db.Float)
    new = db.Column(db.Boolean)
    rating = db.Column(db.String(40))
    win = db.Column(db.Boolean)

    @property
    def xml(self):
        return PlayerXMLDataset(username=self.playerdataset.username, userid=self.playerdataset.userid,
                                name=self.playerdataset.name, position=self.position, colour=self.colour,
                                score=float(self.score), new=self.new, rating=self.rating, win=self.win)

    @xml.setter
    def xml(self, val):
        self.position = val.position
        self.colour = val.colour
        self.score = float(val.score)
        self.new = val.new
        self.rating = val.rating
        self.win = val.win
        self.playerdataset = PlayerDataset.query.filter_by(name=val.name).first()
        if self.playerdataset is None:
            self.playerdataset = PlayerDataset(xml=val)


if __name__ == "__main__":
    tmp = PlaysXMLDataset()
    tmp.gameid = 99
    tmp.game_name = "Hello World"

    data = GameDataset(xml=tmp)
