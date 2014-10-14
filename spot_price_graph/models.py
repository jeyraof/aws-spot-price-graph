# -*- coding: utf-8 -*-


from datetime import datetime
from settings import TIMESTAMP_FORMAT
from spot_price_graph.web import db


class SpotPriceLog(db.Model):
    __tablename__ = u'spot_price_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instance_type = db.Column(db.Unicode(20), nullable=False, index=True)
    spot_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.Unicode(20), nullable=False, index=True)
    availability_zone = db.Column(db.Unicode(20), nullable=False, index=True)
    changed_at = db.Column(db.DateTime, nullable=False, index=True)

    def __init__(self, **kwargs):
        self.instance_type = kwargs.get(u'InstanceType', u'')
        self.spot_price = float(kwargs.get(u'SpotPrice', 0))
        self.product_description = kwargs.get(u'ProductDescription', u'')
        self.availability_zone = kwargs.get(u'AvailabilityZone', u'')
        self.changed_at = datetime.strptime(kwargs.get(u'Timestamp',
                                                       datetime.utcnow().strftime(TIMESTAMP_FORMAT)),
                                            TIMESTAMP_FORMAT)
