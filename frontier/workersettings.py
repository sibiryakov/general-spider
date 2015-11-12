# -*- coding: utf-8 -*-
from distributed_frontera.settings.default_settings import MIDDLEWARES

MAX_NEXT_REQUESTS = 512

#--------------------------------------------------------
# Url storage
#--------------------------------------------------------
BACKEND = 'distributed_frontera.backends.hbase.HBaseBackend'


MIDDLEWARES.extend([
    'frontera.contrib.middlewares.domain.DomainMiddleware',
    'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
])

#--------------------------------------------------------
# Logging
#--------------------------------------------------------
LOGGING_EVENTS_ENABLED = False
LOGGING_MANAGER_ENABLED = True
LOGGING_BACKEND_ENABLED = True
LOGGING_DEBUGGING_ENABLED = False


