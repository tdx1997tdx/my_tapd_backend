ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | sudo xargs kill -9
nohup /usr/local/python3/bin/gunicorn my_tapd_backend.wsgi -w 4 -b 0.0.0.0:8080 &
