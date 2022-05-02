import os

os.system('killall gunicorn')
os.system('/usr/local/python3/bin/gunicorn my_tapd_backend.wsgi -w 4 -b 0.0.0.0:8080')
