import os

if os.environ.get('ENV', None):
    from .prd_settings import *
else:
    from .dev_settings import *
