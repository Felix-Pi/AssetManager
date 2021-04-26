from app import add_symbol, add_transaction
from app.models.Asset import *
from app.models.Portfolio import *
from app.models.User import *


def commit(list):
    db.session.add_all(list)
    db.session.commit()


def users():
    users = [
        User(prename='Felix', surname='Pieschka', email='felix@felixpi.de'),
        User(prename='Demo', surname='Demo', email='demo@demo.de')
    ]
    commit(users)


def asset_types():
    asset_types = [
        Asset_types(type='Stock'),
        Asset_types(type='Etf'),
        Asset_types(type='Crypto'),
    ]
    commit(asset_types)


def portfolio_types():
    portfolio_types = [
        Portfolio_types(type='Stock'),
        Portfolio_types(type='Etf'),
        Portfolio_types(type='Crypto'),
    ]
    commit(portfolio_types)


def portfolios():
    portfolios = [
        Portfolio(type=1, title='Stocks', user_id=1),
        Portfolio(type=1, title='RiskStocks', user_id=1),
        Portfolio(type=2, title='ETF\'s', user_id=1),
        Portfolio(type=3, title='Crypto', user_id=1),
    ]
    commit(portfolios)


def assets():
    add_symbol('APC.F', 1)
    add_symbol('BAYN.DE', 1)
    add_symbol('3CP.F', 1)
    add_symbol('PAH3.DE', 1)
    add_symbol('LIGHT.AS', 1)
    add_symbol('HFG.DE', 1)
    add_symbol('TL0.DE', 1)
    add_symbol('AMD.F', 1)
    add_symbol('BAS.F', 1)
    add_symbol('ABEA.DE', 1)
    add_symbol('ALV.DE', 1)
    add_symbol('AMZ.DE', 1)
    add_symbol('EOAN.F', 1)
    add_symbol('ENR.DE', 1)
    add_symbol('VNA.F', 1)
    add_symbol('FRE.DE', 1)
    add_symbol('WDP.DE', 1)
    add_symbol('TEF.MC', 1)
    add_symbol('NOA3.F', 1)
    add_symbol('TUI1.F', 1)
    add_symbol('RI1.F', 1)
    add_symbol('RRU.F', 1)
    add_symbol('POQ.BE', 1)
    add_symbol('7BC.F', 1)
    add_symbol('PTNA.F', 1)
    add_symbol('0AL.BE', 1)
    add_symbol('O1E.BE', 1)
    add_symbol('SWQ.F', 1)
    add_symbol('42L.F', 1)
    add_symbol('GSG.F', 1)
    add_symbol('IEMM.AS', 2)
    add_symbol('EUNL.DE', 2)
    add_symbol('RBOT.L', 2)
    add_symbol('IQQH.DE', 2)
    add_symbol('MIOTA-EUR', 3)
    add_symbol('ETH-EUR', 3)
    add_symbol('BTC-EUR', 3)
    add_symbol('DOGE-EUR', 3)


def transactions():
    ts = datetime.now()

    add_transaction(1, 'APC.F', ts, 1, 107.73, 2.0),
    add_transaction(1, 'BAYN.DE', ts, 1, 51.93, 3.0),
    add_transaction(1, '3CP.F', ts, 1, 2.86, 39.0),
    add_transaction(1, 'PAH3.DE', ts, 1, 52.75, 1.0),
    add_transaction(1, 'LIGHT.AS', ts, 1, 38.25, 2.0),
    add_transaction(1, 'HFG.DE', ts, 1, 44.68, 1.0),
    add_transaction(1, 'TL0.DE', ts, 1, 392.65, 0.1143),
    add_transaction(1, 'AMD.F', ts, 1, 49.86, 1.0),
    add_transaction(1, 'BAS.F', ts, 1, 65.76, 0.6843),
    add_transaction(1, 'ABEA.DE', ts, 1, 1358.13, 0.022),
    add_transaction(1, 'ALV.DE', ts, 1, 206.4, 0.1452),
    add_transaction(1, 'AMZ.DE', ts, 1, 2654.95, 0.0111),
    add_transaction(1, 'EOAN.F', ts, 1, 9.07, 3.0874),
    add_transaction(1, 'ENR.DE', ts, 1, 29.99, 1.0),
    add_transaction(1, 'VNA.F', ts, 1, 56.36, 0.3548),
    add_transaction(1, 'FRE.DE', ts, 1, 37.05, 0.5398),
    add_transaction(1, 'WDP.DE', ts, 1, 159.85, 0.1251),
    add_transaction(1, 'TEF.MC', ts, 1, 4.16, 5.0),
    add_transaction(1, 'NOA3.F', ts, 1, 4.14, 5.0),
    add_transaction(1, 'TUI1.F', ts, 1, 4.79, 3.0),
    add_transaction(1, 'RI1.F', ts, 1, 13.98, 1.0),
    add_transaction(1, 'RRU.F', ts, 1, 1.386, 5.0),
    add_transaction(2, 'POQ.BE', ts, 1, 0.0382, 1400.0),
    add_transaction(2, '7BC.F', ts, 1, 0.806, 40.0),
    add_transaction(2, 'PTNA.F', ts, 1, 0.664, 34.0),
    add_transaction(2, '0AL.BE', ts, 1, 1.896, 10.0),
    add_transaction(2, 'O1E.BE', ts, 1, 0.0137, 1500.0),
    add_transaction(2, 'SWQ.F', ts, 1, 0.196, 50.0),
    add_transaction(2, '42L.F', ts, 1, 0.042, 250.0),
    add_transaction(2, 'GSG.F', ts, 1, 0.017, 250.0),
    add_transaction(3, 'IEMM.AS', ts, 1, 43.65, 0.7789),
    add_transaction(3, 'EUNL.DE', ts, 1, 67.41, 0.2225),
    add_transaction(3, 'RBOT.L', ts, 1, 10.67, 1.4058),
    add_transaction(3, 'IQQH.DE', ts, 1, 15.9, 1.0),
    add_transaction(4, 'MIOTA-EUR', ts, 1, 0.35, 129.0),
    add_transaction(4, 'ETH-EUR', ts, 1, 952.0, 0.08),
    add_transaction(4, 'BTC-EUR', ts, 1, 31044.0, 0.00313547),
    add_transaction(4, 'DOGE-EUR', ts, 1, 0.079963, 599.64747331),
    add_transaction(1, 'APC.F', ts, 1, 107.73, 0.1),
    add_transaction(1, 'APC.F', ts, 2, 107.73, 0.1),


def init_all():
    users()
    asset_types()
    assets()
    portfolio_types()
    portfolios()
    transactions()


if __name__ == '__main__':
    init_all()
    # transactions()
