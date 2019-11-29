from . import db, Model


class Index(db.Model, Model):
    __tablename__ = "t_ff_index"
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    windcode =db.Column(db.String(12), nullable=False, index=True)
    sec_name = db.Column(db.String(45), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    kind = db.Column(db.String(20), nullable=False, default="normal")


class IndexClosePrice(db.Model, Model):
    __tablename__ = "t_ff_index_cp"
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    windcode = db.Column(db.String(12), db.ForeignKey("t_ff_index.windcode"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    close = db.Column(db.Float)

    info = db.relationship("Index", backref="close")
