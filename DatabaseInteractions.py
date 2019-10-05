from DatabaseModels import PlayDataset
from DatabaseModels import db

def update_database(play):
    playdataset = PlayDataset.query.order_by(PlayDataset.date.desc()).limit(1).all()
    if play.date > playdataset.date:
        return True
    else:
        return False

def update_data(plays):
    PlayDataset.query.order_by(PlayDataset.date.desc()).limit(1).all()
    for play in plays:

        PlayDataset.query.filter_py(id=play.id).first()

def rebuild_database():
    db.drop_all()
    db.create_all()


def load_database():
    rtn = []
    query_data = db.session.query(PlayDataset).all()
    for data in query_data:
        rtn.append(data.xml)
    return rtn


def load_data_into_database(plays):
    for play in plays:
        playdataset = PlayDataset(xml=play)
        db.session.add(playdataset)
        db.session.commit()
