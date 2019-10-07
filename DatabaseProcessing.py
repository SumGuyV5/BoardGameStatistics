from DatabaseModels import PlayDataset
from DatabaseModels import PlayerDataset
from DatabaseModels import PlayersPlayDataset
from DatabaseModels import GameDataset
from app import db


def win_percentage(ignore):
    val = {}
    data = processing(ignore, win_per_processing)
    for key, value in data.items():
        val[key] = 100 * float(value[0]) / float(value[0] + value[1])
    return val


def h_index(ignore):
    data = processing(ignore, h_index_processing)
    return data


def total_games(ignore):
    val = {}
    data = processing(ignore, total_games_processing)
    for key, value in data.items():
        val[key] = value[0]
    return val


def win_count(ignore):
    val = {}
    data = processing(ignore, win_count_processing)
    for key, value in data.items():
        val[key] = value[0]
    return val


def loss_count(ignore):
    val = {}
    data = processing(ignore, loss_count_processing)
    for key, value in data.items():
        val[key] = value[1]
    return val


def total_points(ignore):
    val = {}
    data = processing(ignore, total_points_processing)
    for key, value in data.items():
        val[key] = value[1]
    return val


def processing(ignore, func):
    data = {}
    plays = db.session.query(PlayDataset).all()
    for play in plays:
        if play.nowinstats is True or play.incomplete is True:
            continue
        for players_play in play.playersplaydataset:
            if players_play.playerdataset.name in ignore:
                continue
            if players_play.playerdataset.name not in data.keys():
                data[players_play.playerdataset.name] = [0, 0]
            func(data, players_play)
    return data


def win_per_processing(data, players_play):
    win_count_processing(data, players_play)
    loss_count_processing(data, players_play)


def h_index_processing(data, players_play):
    val = {}
    name = players_play.playerdataset.name
    d = db.session.query(PlayDataset).join(PlayDataset.playersplaydataset).join(PlayDataset.gamedataset)\
        .join(PlayersPlayDataset.playerdataset)\
        .filter(PlayerDataset.name == name).filter(PlayDataset.incomplete is False)\
        .filter(PlayDataset.nowinstats is False).all()
    for x in d:
        if x.gamedataset.name not in val.keys():
            val[x.gamedataset.name] = 0
        val[x.gamedataset.name] += 1
    for idx, key in enumerate(sorted(val.items(), key=lambda item: (item[1], item[0]), reverse=True)):
        if key[1] <= idx:
            data[name] = idx
            break


def total_games_processing(data, players_play):
    data[players_play.playerdataset.name][0] += 1


def win_count_processing(data, players_play):
    if players_play.win:
        data[players_play.playerdataset.name][0] += 1


def loss_count_processing(data, players_play):
    if players_play.win is False:
        data[players_play.playerdataset.name][1] += 1


def total_points_processing(data, players_play):
    val = {}

    """winners_count = self.winners_count()
    self.players = sorted(self.players, key=lambda players: players.score, reverse=self.__lower_is_better__)
    for idx, player in enumerate(self.players):
        points = 0
        if player.score == 0:
            if player.win:
                points = len(self.players) - winners_count
        elif player.win:
            points = len(self.players) - winners_count
        else:
            points = idx
            if idx > 0 and self.players[idx - 1].score == player.score:
                _, points = list(val.items())[-1]

        val[player.name] = points

    return val"""
