TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

FLASK_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
    'SECRET_KEY': '',
    'DEBUG': True,
}

CELERY_BROKER_URI = 'redis:///'
CELERY_RESULT_URI = 'db+sqlite:///result.db'
CELERY_PERIOD = {
    'minutes': 10,
}