from DatabaseModels import PlayDataset
from DatabaseModels import db


def update_database(play):
    playdataset = PlayDataset.query.order_by(PlayDataset.date.desc()).limit(1).all()
    if play.date > playdataset.date:
        return True
    else:
        return False


def update_data(plays):
    lates_play = PlayDataset.query.order_by(PlayDataset.date.desc()).limit(1).all()
    for play in plays:

        PlayDataset.query.filter_py(id=play.id).first()

def rebuild_database():
    """
    drops all current tables in the database and creates all the new tables.
    :return:
    """
    db.drop_all()
    db.create_all()


def load_database():
    """
    loads all the data in the database into a list of PlaysXMLDataset
    :return: a list of PlaysXMLDataset
    """
    rtn = []
    query_data = db.session.query(PlayDataset).all()
    for data in query_data:
        rtn.append(data.xml)
    return rtn


def load_data_into_database(plays):
    """
    Takes a list of PlaysXMLDataset and puts it into the database. with out check if that record already exists.
    :param plays: list of PlaysXMLDataset
    :return: None
    """
    for play in plays:
        playdataset = PlayDataset(xml=play)
        db.session.add(playdataset)
        db.session.commit()
