from flask_restful import Api, Resource, request, reqparse

from . import rest
from ...models import Asset, AssetIndustry, StockHolding, BondHolding


api = Api(rest, prefix="/asset")


@api.resource("/")
class AssetViews(Resource):
    def get(self):
        windcode = AssetViews.arg_parse()
        asset = self.asset(windcode)
        industry = self.industry(windcode)
        stock = self.stock(windcode)
        bond = self.bond(windcode)
        ret = {
            "asset": asset, "industry": industry, "stock": stock, "bond": bond
        }
        return ret

    @staticmethod
    def arg_parse():
        parser = reqparse.RequestParser()
        parser.add_argument("windcode", type=str)
        args = parser.parse_args()
        windcode = args.get("windcode")
        return windcode

    def asset(self, windcode):
        """资产配置比例"""
        rpt_date = Asset.query.with_entities(Asset.date)\
            .filter(Asset.windcode == windcode).order_by(Asset.windcode.asc()).all()
        rpt_date = [x[0] for x in rpt_date]
        if not rpt_date:
            return
        ret = Asset.query.with_entities(
            Asset.stock, Asset.bond, Asset.fund, Asset.warrant, Asset.cash, Asset.other
        ).filter(Asset.windcode == windcode, Asset.date.in_(rpt_date[-2:])).order_by(Asset.date).all()
        change = [round(ret[-1][i]-ret[0][i], 2) for i in range(0, len(ret[0]))]
        ret = [round(x, 2) for x in ret[-1]]
        names = ["股票", "债券", "基金", "权证", "现金", "其他"]
        ret = [[names[i], ret[i], change[i]] for i in range(0, len(names)) if ret[i] != 0]
        return ret

    def industry(self, windcode):
        """行业配置-针对股票仓位"""
        ai = AssetIndustry
        rpt_date = ai.query.with_entities(ai.date).filter(
            ai.windcode == windcode
        ).order_by(ai.industry, ai.date.desc()).limit(2).all()
        rpt_date = [x[0] for x in rpt_date]
        if not rpt_date:
            return
        latest = ai.query.filter(ai.windcode == windcode, ai.date == rpt_date[0]).order_by(ai.rank).all()
        if sum([x.ratio for x in latest]) == 0:
            return
        prev = ai.query.filter(ai.windcode == windcode, ai.date == rpt_date[-1]).order_by(ai.rank).all()
        change = [round(latest[i].ratio-prev[i].ratio, 2) for i in range(0, len(latest))]
        ret = [[latest[i].industry, round(latest[i].ratio, 2), change[i]] for i in range(0, len(latest)) if latest[i].ratio]
        ret = sorted(ret, key=lambda x: x[1], reverse=True)
        return ret

    def stock(self, windcode):
        """10大重仓股"""
        sh = StockHolding
        latest = sh.query.with_entities(sh.date).filter(sh.windcode == windcode).order_by(sh.date.desc()).first()
        if not latest:
            return
        latest = latest[0]
        ret = sh.query.with_entities(sh.stock_name, sh.ratio, sh.change).filter(
            sh.windcode == windcode, sh.date == latest
        ).order_by(sh.rank).all()
        ret = [[x[0], round(x[1], 2), round(x[2], 2)] for x in ret]
        return ret

    def bond(self, windcode):
        """10大重债券"""
        bh = BondHolding
        latest = bh.query.with_entities(bh.date).filter(bh.windcode == windcode).order_by(bh.date.desc()).first()
        if not latest:
            return
        latest = latest[0]
        ret = bh.query.with_entities(bh.bond_name, bh.ratio, bh.change).filter(
            bh.windcode == windcode, bh.date == latest
        ).order_by(bh.rank).all()
        ret = [[x[0], round(x[1], 2), round(x[2], 2)] for x in ret]
        return ret
