from django.http import HttpResponse
from django.views.generic import View
import json
from .models import User
from utils.http_response_utils import get_response_json
import uuid
import datetime


class Login(View):

    def post(self, request):
        data = json.loads(request.body)
        users = User.objects.filter(username=data.get("username"), password=data.get("password"))
        if len(users):
            user = users[0]
            user.token = str(uuid.uuid4())
            user.fail_time = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
            user.save()
            data = {"token": user.token, "fail_time": user.fail_time}
            return get_response_json("OK", data)
        return get_response_json("LOGINFAIL")


class Regist(View):

    def post(self, request):
        data = json.loads(request.body)
        token = str(uuid.uuid4())
        User.objects.create(username=data.get("username"), password=data.get("password"), token=token)
        return get_response_json("OK")


class Report(View):

    def get(self, request):
        return get_response_json("OK")
