from flask_restful import Api, Resource, marshal_with, reqparse, fields
import pandas as pd

from . import rest
from ...models import Brinson, db


api = Api(rest, prefix="/attr")


@api.resource("/")
class BrinsonViews(Resource):
    source_fields = {
        "id": fields.Integer,
        "windcode": fields.String,
        "industry_code": fields.String,
        "industry_name": fields.String,
        "q1": fields.Float,
        "q2": fields.Float,
        "q3": fields.Float,
        "q4": fields.Float,
        "raa": fields.Float,
        "rss": fields.Float,
        "rin": fields.Float,
        "rto": fields.Float,
        "freq": fields.String,
        "benchmark": fields.String,
        "rpt_date": fields.String
    }

    @marshal_with(source_fields)
    def get(self):
        args = BrinsonViews.arg_parser()
        if args is None:
            return
        windcode = args.get("windcode")
        benchmark = args.get("benchmark")
        freq = args.get("freq")
        rpt_date = args.get("rpt_date")
        if freq == "S":
            ret = Brinson.query.filter(
                Brinson.rpt_date == rpt_date, Brinson.freq == freq, Brinson.windcode == windcode, Brinson.benchmark == benchmark
            ).order_by(Brinson.industry_code).all()
        else:
            ret = multi_period(windcode, benchmark, rpt_date)
            print(ret)
        return ret

    @staticmethod
    def arg_parser():
        parser = reqparse.RequestParser()
        parser.add_argument("windcode", type=str)
        parser.add_argument("benchmark", type=str)
        parser.add_argument("freq", type=str)
        parser.add_argument("rpt_date", type=str)
        args = parser.parse_args()
        windcode = args.get("windcode")
        is_in = Brinson.query.with_entities(Brinson.windcode).filter(Brinson.windcode == windcode).first()
        if not is_in:
            return
        benchmark = args.get("benchmark")
        if benchmark is None:
            benchmark = "000300.SH"

        rpt_date = args.get("rpt_date")
        if rpt_date is None:
            rpt_date = Brinson.query.with_entities(Brinson.rpt_date).filter(
                Brinson.windcode == windcode
            ).order_by(Brinson.rpt_date.desc()).first()[0]
            freq = "S"
        else:
            rpt_date = rpt_date.split(",")
            if len(rpt_date) == 1:
                rpt_date = rpt_date[0]
                freq = "S"
            else:
                freq = "M"
        return {"windcode": windcode, "benchmark": benchmark, "freq": freq, "rpt_date": rpt_date}


@api.resource("/rpt_date")
class RptDateViews(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument("windcode", type=str)
        args = parse.parse_args()
        windcode = args.get("windcode")
        is_in = Brinson.query.with_entities(Brinson.windcode).filter(Brinson.windcode == windcode).first()
        if not is_in:
            return
        dates = Brinson.query.with_entities(db.func.distinct(Brinson.rpt_date)).filter(
            Brinson.windcode == windcode, Brinson.freq == "S", Brinson.benchmark == "000300.SH"
        ).order_by(Brinson.rpt_date.desc()).all()
        dates = [x[0].strftime("%Y-%m-%d") for x in dates]
        benchs = Brinson.query.with_entities(db.func.distinct(Brinson.benchmark)).filter(
            Brinson.rpt_date == dates[0], Brinson.windcode == windcode, Brinson.freq == "S"
        ).all()
        benchs = [x[0] for x in benchs]
        return {"date": dates, "benchmark": benchs}


def multi_period(windcode, benchmark, rpt_date: list):
    """多期brinson模型"""
    b = Brinson
    data = b.query.with_entities(
        b.windcode, b.industry_name, b.industry_code, b.q1, b.q2, b.q3, b.q4, b.rpt_date, b.benchmark
    ).filter(
        b.windcode == windcode, b.freq == "S", b.benchmark == benchmark,
        b.rpt_date.between(rpt_date[0], rpt_date[-1])
    ).all()
    data = pd.DataFrame(data).fillna(0)
    data = data.set_index("industry_code")
    for k in ["q1", "q2", "q3", "q4"]:
        data[k] = data[k] / 100 + 1
    rpts = sorted(list(set(data["rpt_date"])), reverse=True)
    init = data[data["rpt_date"] == rpts[0]]

    for rpt in rpts[1:]:
        other = data[data["rpt_date"] == rpt]
        for k in ["q1", "q2", "q3", "q4"]:
            init[k] *= other[k]
    for k in ["q1", "q2", "q3", "q4"]:
        init[k] = (init[k] - 1)*100

    init = init.reset_index()
    init["rpt_date"] = init["rpt_date"].apply(lambda x: x.strftime("%Y-%m-%d"))

    init["raa"] = init["q2"] - init["q1"]
    init['rss'] = init["q3"] - init["q1"]
    init["rin"] = init["q4"] - init["q3"] - init["q2"] + init["q1"]
    init["rto"] = init["q4"] - init["q1"]
    return init.to_dict(orient="records")


@api.resource("/test")
class MultiPeriodViews(Resource):
    def get(self):
        return multi_period()
