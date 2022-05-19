from django.forms.models import model_to_dict
from django.views.generic import View
import json
from .models import User
from utils.http_response_utils import get_response_json
import uuid
import datetime
from django.core.paginator import Paginator
from my_tapd_backend.settings import BASE_DIR
import os
from django.http import Http404, HttpResponse


class Login(View):

    def post(self, request):
        data = json.loads(request.body)
        users = User.objects.filter(username=data.get("username"), password=data.get("password"))
        if len(users):
            user = users[0]
            user.token = str(uuid.uuid4())
            user.fail_time = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
            user.save()
            data = {"token": user.token, "fail_time": user.fail_time, 'id': user.id}
            return get_response_json("OK", data)
        return get_response_json("LOGINFAIL")


class Regist(View):

    def post(self, request):
        data = json.loads(request.body)
        token = str(uuid.uuid4())
        User.objects.create(username=data.get("username"), nickname=data.get("username"),
                            password=data.get("password"),
                            token=token)
        return get_response_json("OK")


class Report(View):

    def get(self, request):
        return get_response_json("OK")


class GetUserByUsername(View):

    def get(self, request):
        params = request.GET
        user = User.objects.get(username=params.get("username"))
        if user:
            ret = {"id": user.id, 'username': user.username, 'nickname': user.nickname,
                   'introduction': user.introduction,
                   'birthday': user.birthday, 'logo': user.logo}
            return get_response_json("OK", ret)
        return get_response_json("OK", {})


class UpdateUserByUsername(View):

    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(username=data.get("username"))
        if user:
            user.nickname = data.get("nickname")
            user.introduction = data.get("introduction")
            user.birthday = data.get("birthday")
            user.logo = data.get("logo")
            user.save()
        return get_response_json("OK")


class GetUser(View):

    def post(self, request):
        data = json.loads(request.body)
        article = User.objects.all().order_by("-create_time")
        if data.get("username"):
            article = article.filter(title__icontains=data.get("username"))
        if data.get("createTimeZone"):
            article = article.filter(create_time__range=tuple(data.get("createTimeZone")))
        total = len(article)
        paginator = Paginator(article, data.get("pageSize"))
        currentPage = data.get("currentPage")
        try:
            article = paginator.page(currentPage)
        except Exception as e:
            currentPage = 1
            article = paginator.page(currentPage)
        ret_data = {
            "total": total,
            "pageSize": data.get("pageSize"),
            "currentPage": currentPage,
            "data": []
        }
        for i in article:
            tmp = model_to_dict(i)
            tmp['create_time'] = i.create_time
            tmp['update_time'] = i.update_time
            ret_data["data"].append(tmp)
        return get_response_json("OK", ret_data)


class GetImage(View):

    def get(self, request, uri):
        path = os.path.join(BASE_DIR, 'static_file', uri)
        if not os.path.exists(path):
            return HttpResponse("图片资源不存在", status=404)
        file = open(path, "rb")
        return HttpResponse(file.read(), content_type='image/jpg')


class UploadImage(View):

    def post(self, request):
        file = request.FILES.get("file")
        file_name = str(uuid.uuid4()) + "." + str(file).split('.')[-1]
        path = os.path.join(BASE_DIR, 'static_file', file_name)
        with open(path, 'wb') as f:
            # 3.获取上传文件的内容并写到创建的文件中
            for content in file.chunks():  # pic.chunks() 上传文件的内容。
                f.write(content)
        return get_response_json("OK", {"path": "getImage/" + file_name})
