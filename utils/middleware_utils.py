from django.middleware.common import MiddlewareMixin
from .log_utils import loggings
from .http_response_utils import R
from django.http.response import JsonResponse
import traceback
import datetime
from app.user.models import User
from utils.http_response_utils import get_response_json


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        # 异常处理
        err_msg = "url:%s,Error:%s" % (request.path_info, traceback.format_exc())
        loggings.error(err_msg)
        return JsonResponse(R.server_error(err_msg))


class TokenMiddleware(MiddlewareMixin):
    """token验证中间件"""
    uri_list = ['/api/login', '/api/regist', '/api/getImage', '/api/uploadImage']

    def process_request(self, request):
        is_pass = True
        for i in TokenMiddleware.uri_list:
            if i in request.path_info:
                is_pass = False
        if is_pass:
            token = request.META.get("HTTP_AUTHORIZATION")
            user_name = request.META.get("HTTP_LOGINNAME")
            if not (token and user_name):
                return get_response_json('AFAIL')
            users = User.objects.filter(username=user_name)
            if not users:
                return get_response_json('AFAIL')
            user = users[0]
            if user.token != token or user.fail_time < datetime.datetime.now():
                return get_response_json('AFAIL')
