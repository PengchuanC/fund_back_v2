from back_server.models import Model, db


class Brinson(db.Model, Model):
    __tablename__ = "t_ff_brinson"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    windcode = db.Column(db.String(12), nullable=False, index=True)
    industry_code = db.Column(db.String(2), nullable=False)
    industry_name = db.Column(db.String(4), nullable=False)
    q1 = db.Column(db.Float)
    q2 = db.Column(db.Float)
    q3 = db.Column(db.Float)
    q4 = db.Column(db.Float)
    raa = db.Column(db.Float)
    rss = db.Column(db.Float)
    rin = db.Column(db.Float)
    rto = db.Column(db.Float)
    freq = db.Column(db.String(2), default="S")
    benchmark = db.Column(db.String(12), nullable=False)
    rpt_date = db.Column(db.Date, nullable=False)
