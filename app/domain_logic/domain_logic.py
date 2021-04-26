from app import db, Asset


def get_symbol(symbol):
    return db.session.query(Asset).filter_by(symbol=symbol).first()

