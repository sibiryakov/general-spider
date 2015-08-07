from distributed_frontera.settings.default_settings import MIDDLEWARES

MAX_REQUESTS = 0
MAX_NEXT_REQUESTS = 128
CONSUMER_BATCH_SIZE = 512
NEW_BATCH_DELAY = 30.0


#--------------------------------------------------------
# Url storage
#--------------------------------------------------------
BACKEND = 'distributed_frontera.backends.hbase.HBaseBackend'
HBASE_DROP_ALL_TABLES = False
HBASE_THRIFT_PORT = 9090
HBASE_THRIFT_HOST = 'localhost'
HBASE_QUEUE_PARTITIONS = 2

MIDDLEWARES.extend([
    'frontera.contrib.middlewares.domain.DomainMiddleware',
    'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
])

KAFKA_LOCATION = 'localhost:9092'
FRONTIER_GROUP = 'scrapy-crawler'
INCOMING_TOPIC = 'frontier-done'
OUTGOING_TOPIC = 'frontier-todo'
SCORING_GROUP = 'scrapy-scoring'
SCORING_TOPIC = 'frontier-score'

#--------------------------------------------------------
# Logging
#--------------------------------------------------------
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = True
LOGGING_BACKEND_ENABLED = True
LOGGING_DEBUGGING_ENABLED = False


