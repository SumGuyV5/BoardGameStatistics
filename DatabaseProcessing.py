from DatabaseModels import PlayDataset
from DatabaseModels import PlayerDataset
from DatabaseModels import PlayersPlayDataset
from app import db


players = ['Tanya', 'Richard Allen', 'Damon', 'Jeff', 'Terry', 'Arden', 'Charlene', 'Julie', 'Alex', 'Tim',
           'Dimetre', 'Shelly']


def win_percentage():
    val = {}
    data = processing(win_per_processing)
    for key, value in data.items():
        val[key] = 100 * float(value[0]) / float(value[0] + value[1])
    return val


def h_index():
    return h_index_processing()


def total_games():
    val = {}
    data = processing(total_games_processing)
    for key, value in data.items():
        val[key] = value[0]
    return val


def win_count():
    val = {}
    data = processing(win_count_processing)
    for key, value in data.items():
        val[key] = value[0]
    return val


def loss_count():
    val = {}
    data = processing(loss_count_processing)
    for key, value in data.items():
        val[key] = value[1]
    return val


def total_points():
    return total_points_processing()


def points_per_game():
    val = {}
    total_gs = total_games()
    total_ps = total_points()

    for key, value in total_gs.items():
        val[key] = round(float(total_ps[key] / value), 2)
    return val


def processing(func):
    data = {}
    plays = db.session.query(PlayDataset).all()
    for play in plays:
        if play.nowinstats is True or play.incomplete is True:
            continue
        for players_play in play.playersplaydataset:
            if players_play.playerdataset.name in players:
                if players_play.playerdataset.name not in data.keys():
                    data[players_play.playerdataset.name] = [0, 0]
                func(data, players_play)
    return data


def win_per_processing(data, players_play):
    win_count_processing(data, players_play)
    loss_count_processing(data, players_play)


def h_index_processing():
    val = {}
    for player in players:
        query = db.session.query(PlayDataset)\
            .join(PlayDataset.playersplaydataset)\
            .join(PlayDataset.gamedataset)\
            .join(PlayersPlayDataset.playerdataset)\
            .filter(PlayerDataset.name == player)\
            .all()
        val[player] = 0
        tmp = {}
        for play in query:
            if play.nowinstats is True or play.incomplete is True:
                continue
            if play.gamedataset.name not in tmp.keys():
                tmp[play.gamedataset.name] = 0
            tmp[play.gamedataset.name] += 1

        for idx, key in enumerate(sorted(tmp.items(), key=lambda item: (item[1], item[0]), reverse=True)):
            if key[1] <= idx:
                val[player] = idx
                break
    return val


def total_games_processing(data, players_play):
    data[players_play.playerdataset.name][0] += 1


def win_count_processing(data, players_play):
    if players_play.win:
        data[players_play.playerdataset.name][0] += 1


def loss_count_processing(data, players_play):
    if players_play.win is False:
        data[players_play.playerdataset.name][1] += 1


def total_points_processing():
    val = {el: 0 for el in players}
    query = db.session.query(PlayDataset) \
        .join(PlayDataset.playersplaydataset) \
        .join(PlayDataset.gamedataset) \
        .join(PlayersPlayDataset.playerdataset) \
        .filter(PlayerDataset.name.in_(players)) \
        .all()

    for play in query:
        tmp = {}
        if play.nowinstats is True or play.incomplete is True:
            continue
        winners_count = 0
        for players_play in play.playersplaydataset:
            if players_play.won:
                winners_count += 1
        reverse = False
        if play.gamedataset.name == 'No Thanks!':
            reverse = True
        players_sort = sorted(play.playersplaydataset, key=lambda playersplaydataset: playersplaydataset.score,
                              reverse=reverse)
        for idx, players_play in enumerate(players_sort):
            player_name = players_play.playerdataset.name
            points = 0
            if players_play.score == 0:
                if players_play.won:
                    points = len(players_sort) - winners_count
            elif players_play.won:
                points = len(players_sort) - winners_count
            else:
                points = idx
                if idx > 0 and players_sort[idx - 1].score == players_play.score:
                    _, points = list(tmp.items())[-1]

            tmp[player_name] = points
            if player_name in players:
                val[player_name] += points
    return val
