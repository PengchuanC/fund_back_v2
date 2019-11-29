from back_server.models import Model, db


class Asset(Model, db.Model):
    __tablename__ = "t_ff_asset"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    windcode = db.Column(db.String(10), db.ForeignKey('t_ff_funds.windcode'), nullable=False, index=True)
    stock = db.Column(db.Float, nullable=False, default=0.0)
    bond = db.Column(db.Float, nullable=False, default=0.0)
    fund = db.Column(db.Float, nullable=False, default=0.0)
    warrant = db.Column(db.Float, nullable=False, default=0.0)
    cash = db.Column(db.Float, nullable=False, default=0.0)
    other = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False, index=True)


class AssetIndustry(db.Model, Model):
    __tablename__ = "t_ff_asset_industry"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    windcode = db.Column(db.String(10), nullable=False, index=True)
    industry = db.Column(db.String(4), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    ratio = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False)


class StockHolding(db.Model, Model):
    __tablename__ = "t_ff_asset_stock"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    windcode = db.Column(db.String(10), nullable=False)
    stock_code = db.Column(db.String(6), nullable=False)
    stock_name = db.Column(db.String(8), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    ratio = db.Column(db.Float)
    change = db.Column(db.Float)
    date = db.Column(db.Date)


class BondHolding(db.Model, Model):
    __tablename__ = "t_ff_asset_bond"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    windcode = db.Column(db.String(10), nullable=False)
    bond_code = db.Column(db.String(6), nullable=False)
    bond_name = db.Column(db.String(8), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    ratio = db.Column(db.Float)
    change = db.Column(db.Float)
    date = db.Column(db.Date)
