# -*- coding: utf-8 -*-

import flask
from celery import Celery
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from settings import (FLASK_CONFIG, TIMESTAMP_FORMAT,
                      CELERY_BROKER_URI, CELERY_RESULT_URI, CELERY_PERIOD)
from spot_price_graph.api import AWSAPIWrapper
from datetime import datetime, timedelta

app = flask.Flask(__name__)
app.config.update(FLASK_CONFIG)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)

celery = Celery(main='spot_price',
                backend=CELERY_RESULT_URI,
                broker=CELERY_BROKER_URI,)
celery.conf.update(
    CELERY_TIMEZONE='UTC',
    CELERY_ENABLE_UTC=True,
    CELERYBEAT_SCHEDULE={
        'crawl-spot-price-every-hour': {
            'task': 'spot_price_graph.web.crawl_spot_price',
            'schedule': timedelta(**CELERY_PERIOD),
        }
    }
)


# Views
@app.route("/")
def index():
    return '1'


# Models
class SpotPriceLog(db.Model):
    __tablename__ = u'spot_price_log'
    __table_args__ = (db.UniqueConstraint('instance_type',
                                          'product_description',
                                          'availability_zone',
                                          'changed_at',
                                          name='log_uc'), )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instance_type = db.Column(db.Unicode(20), nullable=False, index=True)
    spot_price = db.Column(db.Float, nullable=False)
    product_description = db.Column(db.Unicode(20), nullable=False, index=True)
    availability_zone = db.Column(db.Unicode(20), nullable=False, index=True)
    changed_at = db.Column(db.DateTime, nullable=False, index=True)

    def __init__(self, **kwargs):
        super(SpotPriceLog, self).__init__(**kwargs)

    @staticmethod
    def parse_result(result):
        return {
            'instance_type': result.get(u'InstanceType', u''),
            'spot_price': float(result.get(u'SpotPrice', 0)),
            'product_description': result.get(u'ProductDescription', u''),
            'availability_zone': result.get(u'AvailabilityZone', u''),
            'changed_at': datetime.strptime(result.get(u'Timestamp',
                                                       datetime.utcnow().strftime(TIMESTAMP_FORMAT)),
                                            TIMESTAMP_FORMAT),
        }

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = cls.query.filter_by(**kwargs).first()
        if not instance:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
        return instance


# Celery
@celery.task
def crawl_spot_price():
    api = AWSAPIWrapper()
    query = api.ec2.describe_spot_price_history(instance_types=[],
                                                start_time=datetime.utcnow() - timedelta(hours=1, minutes=15),
                                                )
    result = api.command(query)
    save_spot_price_history(result)


def save_spot_price_history(result):
    result_list = result.get(u'SpotPriceHistory', [])
    result_storage = []
    for result in result_list:
        result_storage.append(SpotPriceLog.get_or_create(**SpotPriceLog.parse_result(result)))