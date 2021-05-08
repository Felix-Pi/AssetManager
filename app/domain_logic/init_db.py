from app import add_symbol, add_transaction
from app.models.Asset import *
from app.models.Portfolio import *
from app.models.User import *


def commit(list):
    db.session.add_all(list)
    db.session.commit()


def users():
    users = [
        User(username='Felix Pieschka', email='felix@felixpi.de', password_hash=generate_password_hash('password')),
    ]
    commit(users)


def asset_types():
    asset_types = [
        Asset_types(type='EQUITY'),
        Asset_types(type='ETF'),
        Asset_types(type='CRYPTOCURRENCY'),
        Asset_types(type='CURRENCY'),
        Asset_types(type='UNKNOWN'),
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
        Portfolio(type=1, title='Stocks', user_id=1, value=1),
        Portfolio(type=1, title='RiskStocks', user_id=1, value=1),
        Portfolio(type=2, title='ETF\'s', user_id=1, value=1),
        Portfolio(type=3, title='Crypto', user_id=1, value=1),
    ]
    commit(portfolios)


def assets():
    # add_symbol('USDEUR=X', 4)
    pass


def transactions():
    transaction_types = [
        Transaction_types(title='Bought', suffix='Transactions', sort='4'),
        Transaction_types(title='Sold', suffix='Transactions', sort='3'),
        Transaction_types(title='Monthly payment', suffix='€', sort='5'),
        Transaction_types(title='Money Transfer', suffix='€', sort='2'),
        Transaction_types(title='Dividend payment', suffix='€', sort='1'),
    ]
    commit(transaction_types)

    add_transaction(pf_id=2, symbol='RRU.F', transcation_type=1, quantity=3.641, price=1,
                    timestamp="03.06.20")  # RollsRoyce
    add_transaction(pf_id=1, symbol='AZK.F', transcation_type=1, quantity=15, price=0.767,
                    timestamp="03.06.20")  # Hertz
    add_transaction(pf_id=1, symbol='PAH3.DE', transcation_type=1, quantity=1, price=52.34,
                    timestamp="03.06.20")  # Porsche
    add_transaction(pf_id=2, symbol='TCO0.DE', transcation_type=1, quantity=1, price=2.574,
                    timestamp="04.06.20")  # Tesco
    add_transaction(pf_id=1, symbol='AZK.F', transcation_type=2, quantity=15, price=4.643,
                    timestamp="09.06.20")  # Hertz
    add_transaction(pf_id=1, symbol='SIX2.DE', transcation_type=1, quantity=1, price=51.80,
                    timestamp="09.06.20")  # Sixt
    add_transaction(pf_id=1, symbol='AMD.F', transcation_type=1, quantity=1, price=48.855, timestamp="16.06.20")  # AMD
    add_transaction(pf_id=1, symbol='EOAN.F', transcation_type=1, quantity=3, price=9.818, timestamp="16.06.20")  # EON
    add_transaction(pf_id=1, symbol='IFX.DE', transcation_type=1, quantity=1, price=19.79,
                    timestamp="16.06.20")  # Infineon
    add_transaction(pf_id=1, symbol='SIX2.DE', transcation_type=5, quantity=1, price=0.04, timestamp="27.06.20")  # Sixt
    add_transaction(pf_id=3, symbol='IQQW.F', transcation_type=3, quantity=0.5889, price=42.45,
                    timestamp="02.07.20")  # MSCIWorld'
    add_transaction(pf_id=1, symbol='DTE.DE', transcation_type=1, quantity=1, price=15.15,
                    timestamp="15.07.20")  # DeutscheTelekom
    add_transaction(pf_id=1, symbol='BAYN.DE', transcation_type=1, quantity=1, price=56.88,
                    timestamp="04.08.20")  # Bayer
    add_transaction(pf_id=2, symbol='3QO.BE', transcation_type=1, quantity=12, price=0.425,
                    timestamp="05.08.20")  # ZionOil
    add_transaction(pf_id=2, symbol='RRU.F', transcation_type=2, quantity=1, price=2.894,
                    timestamp='24.08.20')  # RollsRoyce
    add_transaction(pf_id=2, symbol='TCO0.DE', transcation_type=2, quantity=1, price=2.546,
                    timestamp='24.08.20')  # Tesco
    add_transaction(pf_id=1, symbol='SIX2.DE', transcation_type=2, quantity=1, price=47.45,
                    timestamp='24.08.20')  # Sixt
    add_transaction(pf_id=1, symbol='APC.F', transcation_type=1, quantity=4, price=107.457,
                    timestamp='24.08.20')  # Apple
    add_transaction(pf_id=3, symbol='IQQW.F', transcation_type=2, quantity=0.5889, price=43.449,
                    timestamp='24.08.20')  # MSCIWorld
    add_transaction(pf_id=1, symbol='SNH.F', transcation_type=1, quantity=125, price=0.048,
                    timestamp='24.08.20')  # SteinhoffInternational
    add_transaction(pf_id=1, symbol='3CP.F', transcation_type=1, quantity=1, price=2.1975,
                    timestamp='26.08.20')  # Xiaomi
    add_transaction(pf_id=1, symbol='3CP.F', transcation_type=1, quantity=10, price=2.197,
                    timestamp='26.08.20')  # Xiaomi
    # # 'SPLITAppleAktie', '28.08'
    add_transaction(pf_id=1, symbol='3CP.F', transcation_type=1, quantity=3, price=2.93, timestamp='01.09.20')  # Xiaomi
    add_transaction(pf_id=1, symbol='3CP.F', transcation_type=1, quantity=7, price=2.933,
                    timestamp='01.09.20')  # Xiaomi
    add_transaction(pf_id=1, symbol='TL0.DE', transcation_type=3, quantity=0.0263, price=378.95,
                    timestamp="16.09.20")  # Tesla'
    add_transaction(pf_id=1, symbol='IFX.DE', transcation_type=2, quantity=1, price=24.225,
                    timestamp="18.09.20")  # Infineon
    add_transaction(pf_id=1, symbol='DTE.DE', transcation_type=2, quantity=1, price=14.54,
                    timestamp="21.09.20")  # DeutscheTelekom
    add_transaction(pf_id=1, symbol='UAL1.F', transcation_type=1, quantity=1, price=29.0,
                    timestamp="21.09.20")  # UnitedAirlines
    add_transaction(pf_id=1, symbol='APC.F', transcation_type=2, quantity=1, price=99.20, timestamp="01.10.20")  # Apple
    add_transaction(pf_id=1, symbol='PAH3.DE', transcation_type=1, quantity=1, price=51.16,
                    timestamp="01.10.20")  # Porsche
    add_transaction(pf_id=1, symbol='BAYN.DE', transcation_type=2, quantity=1, price=50.75,
                    timestamp="01.10.20")  # Bayer
    add_transaction(pf_id=1, symbol='BAYN.DE', transcation_type=1, quantity=2, price=51.25,
                    timestamp="01.10.20")  # Bayer
    add_transaction(pf_id=1, symbol='SNH.F', transcation_type=2, quantity=125, price=0.0365,
                    timestamp="1.10.20")  # SteinhoffInternational
    add_transaction(pf_id=1, symbol='ABEA.DE', transcation_type=3, quantity=0.0079, price=1253.60,
                    timestamp="02.10.20")  # AlphabetA'
    add_transaction(pf_id=1, symbol='AMZ.DE', transcation_type=3, quantity=0.0036, price=2710.50,
                    timestamp="02.10.20")  # Amazon'
    add_transaction(pf_id=1, symbol='TL0.DE', transcation_type=3, quantity=0.0269, price=370.90,
                    timestamp="02.10.20")  # Tesla'
    add_transaction(pf_id=1, symbol='PAH3.DE', transcation_type=5, quantity=1, price=4.42,
                    timestamp="06.10.20")  # Porsche
    add_transaction(pf_id=1, symbol='UAL1.F', transcation_type=2, quantity=1, price=29.00,
                    timestamp="15.10.20")  # UnitedAirlines
    add_transaction(pf_id=2, symbol='3QO.BE', transcation_type=2, quantity=12, price=0.344,
                    timestamp="15.10.20")  # ZionOil
    add_transaction(pf_id=1, symbol='LIGHT.AS', transcation_type=1, quantity=1, price=35.55,
                    timestamp="15.10.20")  # Signify
    add_transaction(pf_id=1, symbol='ABEA.DE', transcation_type=3, quantity=0.0071, price=1406.80,
                    timestamp="02.11.20")  # AlphabetA'
    add_transaction(pf_id=1, symbol='AMZ.DE', transcation_type=3, quantity=0.0038, price=2624.00,
                    timestamp="02.11.20")  # Amazon'
    add_transaction(pf_id=1, symbol='TL0.DE', transcation_type=3, quantity=0.0290, price=343.65,
                    timestamp="02.11.20")  # Tesla'
    add_transaction(pf_id=1, symbol='HFG.DE', transcation_type=1, quantity=1, price=43.68,
                    timestamp="09.11.20")  # HelloFresh
    add_transaction(pf_id=1, symbol='APC.F', transcation_type=5, quantity=1, price=0.44, timestamp="19.11.20")  # Apple
    add_transaction(pf_id=1, symbol='BAS.F', transcation_type=3, quantity=0.2481, price=60.45,
                    timestamp="02.12.20")  # BASF'
    add_transaction(pf_id=1, symbol='TL0.DE', transcation_type=3, quantity=0.0321, price=466.10,
                    timestamp="02.12.20")  # Tesla'
    add_transaction(pf_id=1, symbol='3CP.F', transcation_type=1, quantity=8, price=2.65, timestamp="02.12.20")  # Xiaomi
    add_transaction(pf_id=2, symbol='7BC.F', transcation_type=1, quantity=40, price=0.695,
                    timestamp="29.12.20")  # BevCanna
    add_transaction(pf_id=1, symbol='ALV.DE', transcation_type=3, quantity=0.0499, price=200.25,
                    timestamp="04.01.21")  # Allianz'
    add_transaction(pf_id=1, symbol='BAS.F', transcation_type=3, quantity=0.1524, price=65.60,
                    timestamp="04.01.21")  # BASF'
    add_transaction(pf_id=1, symbol='EOAN.F', transcation_type=3, quantity=1.0874, price=9.20,
                    timestamp="04.01.21")  # EON'
    add_transaction(pf_id=1, symbol='ABEA.DE', transcation_type=3, quantity=0.007, price=11427.20,
                    timestamp="04.01.21")  # AlphabetA'
    add_transaction(pf_id=1, symbol='AMZ.DE', transcation_type=3, quantity=0.0037, price=2632.50,
                    timestamp="04.01.21")  # Amazon'
    add_transaction(pf_id=2, symbol='NJTC.BE', transcation_type=1, quantity=15, price=1.07,
                    timestamp="08.01.21")  # Polarityte
    add_transaction(pf_id=1, symbol='3CP.F', transcation_type=1, quantity=10, price=3.082,
                    timestamp="14.01.21")  # Xiaomi
    add_transaction(pf_id=2, symbol='A9K.F', transcation_type=1, quantity=41, price=0.0647,
                    timestamp="19.01.21")  # HaloLabs
    add_transaction(pf_id=2, symbol='NJTC.BE', transcation_type=2, quantity=15, price=0.84,
                    timestamp="21.01.21")  # Polarityte
    add_transaction(pf_id=2, symbol='7BC.F', transcation_type=2, quantity=40, price=0.55,
                    timestamp="25.01.21")  # BevCanna
    add_transaction(pf_id=1, symbol='NOA3.F', transcation_type=1, quantity=5, price=3.936,
                    timestamp="25.01.21")  # Nokia
    add_transaction(pf_id=1, symbol='5G5.F', transcation_type=1, quantity=1, price=8.49, timestamp="27.01.21")  # GOPRO
    add_transaction(pf_id=1, symbol='5G5.F', transcation_type=2, quantity=1, price=7.50, timestamp="29.01.21")  # GOPRO
    add_transaction(pf_id=1, symbol='EOAN.F', transcation_type=2, quantity=3, price=8.77, timestamp="29.01.21")  # EON
    add_transaction(pf_id=2, symbol='AH9.F', transcation_type=1, quantity=1, price=10.40, timestamp="29.01.21")  # AMC
    add_transaction(pf_id=2, symbol='RI1.F', transcation_type=1, quantity=1, price=12.984,
                    timestamp="29.01.21")  # BlackBerry
    add_transaction(pf_id=1, symbol='APC.F', transcation_type=2, quantity=1, price=112.56,
                    timestamp="03.02.21")  # Apple
    add_transaction(pf_id=1, symbol='BAYN.DE', transcation_type=1, quantity=1, price=51.29,
                    timestamp="03.02.21")  # Bayer
    add_transaction(pf_id=1, symbol='LIGHT.AS', transcation_type=1, quantity=1, price=38.94,
                    timestamp="03.02.21")  # Signify
    add_transaction(pf_id=3, symbol='IQQH.DE', transcation_type=1, quantity=1, price=14.90,
                    timestamp="03.02.21")  # GlobalCleanEnergy
    add_transaction(pf_id=1, symbol='APC.F', transcation_type=5, quantity=1, price=0.29, timestamp="13.02.21")  # Apple
    add_transaction(pf_id=2, symbol='7BC.F', transcation_type=1, quantity=15, price=0.94,
                    timestamp="15.02.21")  # BevCanna
    add_transaction(pf_id=2, symbol='GSG.F', transcation_type=1, quantity=250, price=0.013,
                    timestamp="17.02.21")  # ShengloOil
    add_transaction(pf_id=2, symbol='42L.F', transcation_type=1, quantity=250, price=0.038,
                    timestamp="17.02.21")  # IntlCobaltCorp
    add_transaction(pf_id=2, symbol='SWQ.F', transcation_type=1, quantity=50, price=0.176,
                    timestamp="17.02.21")  # SilverMinesLTD
    add_transaction(pf_id=2, symbol='RRU.F', transcation_type=1, quantity=5, price=1.185,
                    timestamp="17.02.21")  # RollsRoyce
    add_transaction(pf_id=1, symbol='TUI1.F', transcation_type=1, quantity=3, price=4.46, timestamp="23.02.21")  # TUI
    add_transaction(pf_id=2, symbol='7BC.F', transcation_type=1, quantity=25, price=0.645,
                    timestamp="26.02.21")  # BevCanna
    add_transaction(pf_id=1, symbol='EOAN.F', transcation_type=1, quantity=2, price=8.506, timestamp="01.03.21")  # EON
    add_transaction(pf_id=1, symbol='WDP.DE', transcation_type=3, quantity=0.0615, price=162.56,
                    timestamp="02.03.21")  # Disney'
    add_transaction(pf_id=1, symbol='VNA.F', transcation_type=3, quantity=0.1854, price=53.92,
                    timestamp="02.03.21")  # Vonovia'
    add_transaction(pf_id=1, symbol='FRE.DE', transcation_type=3, quantity=0.2795, price=35.77,
                    timestamp="02.03.21")  # Fresenius'
    add_transaction(pf_id=1, symbol='BAS.F', transcation_type=3, quantity=0.1445, price=68.70,
                    timestamp="02.03.21")  # BASF'
    add_transaction(pf_id=1, symbol='ALV.DE', transcation_type=3, quantity=0.0492, price=203.05,
                    timestamp="02.03.21")  # Allianz'
    add_transaction(pf_id=1, symbol='ENR.DE', transcation_type=1, quantity=1, price=28.99,
                    timestamp="08.03.21")  # SimensEnergy
    add_transaction(pf_id=1, symbol='TNE5.DE', transcation_type=1, quantity=5, price=3.96,
                    timestamp="11.03.21")  # Telefonica
    add_transaction(pf_id=2, symbol='AH9.F', transcation_type=2, quantity=1, price=11.10, timestamp="15.03.21")  # AMC
    add_transaction(pf_id=1, symbol='PAH3.DE', transcation_type=2, quantity=1, price=85.00,
                    timestamp="17.03.21")  # Porsche
    add_transaction(pf_id=2, symbol='POQ.BE', transcation_type=1, quantity=400, price=0.0242,
                    timestamp="29.03.21")  # 88Energy
    add_transaction(pf_id=2, symbol='0AL.BE', transcation_type=1, quantity=10, price=1.796,
                    timestamp="29.03.21")  # AgileTherapeutics
    add_transaction(pf_id=2, symbol='POQ.BE', transcation_type=1, quantity=1000, price=0.0418,
                    timestamp="31.03.21")  # 88Energy
    add_transaction(pf_id=2, symbol='PTNA.F', transcation_type=1, quantity=34, price=0.615,
                    timestamp="01.04.21")  # PalantinTechnologies
    add_transaction(pf_id=2, symbol='O1E.BE', transcation_type=1, quantity=1500, price=0.013,
                    timestamp="07.04.21")  # OttoEnergy
    add_transaction(pf_id=1, symbol='WDP.DE', transcation_type=3, quantity=0.0636, price=157.18,
                    timestamp="16.04.21")  # Disney
    add_transaction(pf_id=1, symbol='VNA.F', transcation_type=3, quantity=0.1694, price=59.02,
                    timestamp="16.04.21")  # Vonovia
    add_transaction(pf_id=1, symbol='FRE.DE', transcation_type=3, quantity=0.2603, price=38.415,
                    timestamp="16.04.21")  # Fresenius
    add_transaction(pf_id=1, symbol='BAS.F', transcation_type=3, quantity=0.1383, price=72.28,
                    timestamp="16.04.21")  # BASF
    add_transaction(pf_id=1, symbol='ALV.DE', transcation_type=3, quantity=0.0461, price=216.70,
                    timestamp="16.04.21")  # Allianz
    add_transaction(pf_id=3, symbol='IEMM.AS', transcation_type=3, quantity=0.7789, price=44.651,
                    timestamp="16.04.21")  # MSCIEMUSD
    add_transaction(pf_id=3, symbol='EUNL.DE', transcation_type=3, quantity=0.2225, price=67.414,
                    timestamp="16.04.21")  # CoreMSCIWORLD
    add_transaction(pf_id=3, symbol='RBOT.L', transcation_type=3, quantity=1.4058, price=10.67,
                    timestamp="16.04.21")  # Automation&Robotics
    add_transaction(pf_id=4, symbol='ETH-EUR', transcation_type=1, quantity=0.080285, price=952,
                    timestamp="10.01.21")  # ETH
    add_transaction(pf_id=4, symbol='MIOTA-EUR', transcation_type=1, quantity=129, price=0.35,
                    timestamp="07.01.17")  # MIOTA
    add_transaction(pf_id=4, symbol='BTC-EUR', transcation_type=1, quantity=0.00313547, price=31044,
                    timestamp="10.01.21")  # BTC
    add_transaction(pf_id=4, symbol='DOGE-EUR', transcation_type=1, quantity=825.52, price=0.036341,
                    timestamp="01.02.21")  # DOGE
    add_transaction(pf_id=4, symbol='DOGE-EUR', transcation_type=2, quantity=402.56, price=0.0745,
                    timestamp="13.04.21")  # DOGE
    add_transaction(pf_id=4, symbol='DOGE-EUR', transcation_type=2, quantity=123, price=0.245,
                    timestamp="16.04.21")  # DOGE
    add_transaction(pf_id=4, symbol='DOGE-EUR', transcation_type=1, quantity=300, price=0.2,
                    timestamp="17.04.21")  # DOGE

    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=35, timestamp="29.05.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=40, timestamp="03.06.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=100, timestamp="16.06.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=30, timestamp="01.07.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=30, timestamp="03.08.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=30, timestamp="04.08.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=400, timestamp="24.08.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=30, timestamp='01.09.20')
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=30, timestamp="29.09.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=30, timestamp="29.10.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="4.11.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=45, timestamp="30.11.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="03.12.20")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="04.01.21")
    add_transaction(pf_id=4, symbol=None, transcation_type=4, quantity=1, price=100, timestamp="10.01.21", cost=2.66)
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="03.02.21")
    add_transaction(pf_id=4, symbol=None, transcation_type=4, quantity=1, price=30, timestamp="03.02.21", cost=0.0)
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=85, timestamp="26.02.21")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="03.03.21")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=85, timestamp="06.04.21")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="06.04.21")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="06.04.21")
    add_transaction(pf_id=1, symbol=None, transcation_type=4, quantity=1, price=50, timestamp="03.05.21")

    add_transaction(pf_id=1, symbol='BAYN.DE', transcation_type=5, quantity=3, price=2.00, timestamp="29.04.21")
    add_transaction(pf_id=1, symbol='BAS.F', transcation_type=5, quantity=0.6843, price=3.30, timestamp="04.05.21")


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
