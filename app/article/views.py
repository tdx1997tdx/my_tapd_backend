from django.forms.models import model_to_dict
from django.views.generic import View
import json
from .models import Article
from utils.http_response_utils import get_response_json
from django.core.paginator import Paginator


class GetArticle(View):

    def post(self, request):
        data = json.loads(request.body)
        article = Article.objects.all().order_by("-create_time")
        if data.get("user_id"):
            article = article.filter(author_id=data.get("user_id"))
        if data.get("is_delete"):
            article = article.filter(is_delete=data.get("is_delete"))
        if data.get("title"):
            article = article.filter(title__icontains=data.get("title"))
        if data.get("isPublic"):
            article = article.filter(is_public=data.get("isPublic"))
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
            tmp['content'] = tmp['content'][:100]
            tmp['create_time'] = i.create_time
            tmp['update_time'] = i.update_time
            tmp['author_name'] = i.author.nickname
            ret_data["data"].append(tmp)
        return get_response_json("OK", ret_data)


class GetArticleById(View):

    def get(self, request):
        id = request.GET.get("id")
        article = Article.objects.get(id=id)
        article.pv = article.pv + 1
        article.save()
        tmp = model_to_dict(article)
        tmp['create_time'] = article.create_time
        tmp['update_time'] = article.update_time
        tmp['pv'] = article.pv
        tmp['zan'] = article.zan
        tmp['author_name'] = article.author.nickname
        return get_response_json("OK", tmp)


class PublicArticle(View):

    def post(self, request):
        data = json.loads(request.body)
        Article.objects.create(title=data.get("title"), content=data.get("content"), author_id=data.get("author_id"),
                               is_public=data.get("isPublic"), create_time=data.get("createTime"))
        return get_response_json("OK")


class DeleteArticle(View):

    def post(self, request):
        data = json.loads(request.body)
        article = Article.objects.get(id=data.get("id"))
        article.is_delete = data.get("is_delete")
        article.save()
        return get_response_json("OK")


class UpdateArticle(View):

    def post(self, request):
        data = json.loads(request.body)
        article = Article.objects.get(id=data.get("id"))
        article.title = data.get("title")
        article.content = data.get("content")
        article.is_public = data.get("is_public")
        article.save()
        return get_response_json("OK")
