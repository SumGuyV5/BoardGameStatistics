from DatabaseModels import PlayDataset
from DatabaseModels import db


def rebuild_database():
    """
    Drops all current tables in the database and creates all the new tables.
    :return:
    """
    db.drop_all()
    db.create_all()


def number_records():
    return db.session.query(PlayDataset).count()


def update_database_check(play):
    """
    :param play: a PlayXMLDataset.
    :return: True if the passed PlayXMLDataset has a newer date then the news PlayDataset record else False.
    """
    playdataset = PlayDataset.query.order_by(PlayDataset.date.desc()).limit(1).all()
    if play.date > playdataset.date:
        return True
    else:
        return False


def update_records(plays):
    """
    Update a list of play records.
    :param plays: The list of play records to update.
    :return:
    """
    for play in plays:
        update_record(play)


def update_record(play):
    """
    Updates the provide play record.
    :param play: The play record to update.
    :return:
    """
    data = PlayDataset.query.filter_py(id=play.id).first()
    if data is not None:
        data.xml = play
        db.session.commit()


def add_records(plays):
    """
    Takes a list of PlayXMLDatasets check if they are not in the databse and if not adds them.
    :param plays:
    :return:
    """
    for play in plays:
        if PlayDataset.query.filter_by(id=play.id).first() is None:
            add_record(play)


def add_record(play):
    """
    Creates adds, and commits the record.
    :param play:
    :return:
    """
    db.session.add(PlayDataset(xml=play))
    db.session.commit()


def load_database_into_xml():
    """
    Loads all the data in the database into a list of PlaysXMLDataset.
    :return: a list of PlaysXMLDataset.
    """
    rtn = []
    query_data = db.session.query(PlayDataset).all()
    for data in query_data:
        rtn.append(data.xml)
    return rtn


def load_xml_into_database(plays):
    """
    Takes a list of PlaysXMLDataset and puts it into the database. with out check if that record already exists.
    :param plays: list of PlaysXMLDataset.
    :return: None
    """
    for play in plays:
        add_record(play)

