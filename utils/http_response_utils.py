from enum import Enum
from django.http import HttpResponse
import json
import datetime


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class StatusCodeEnum(Enum):
    OK = (0, "成功")
    LOGINFAIL = (10001, "登录失败,账号密码或者密码错误")
    AFAIL = (10002, "鉴权失败")
    ERROR = (-1, "未知错误")
    SERVER_ERR = (500, "程序错误")

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def msg(self):
        """获取状态码信息"""
        return self.value[1]


def get_response_json(type, data=None):
    resp_dict = {}
    resp_dict['code'] = eval('StatusCodeEnum.%s.code' % (type))
    resp_dict['msg'] = eval('StatusCodeEnum.%s.msg' % (type))
    if data:
        resp_dict['data'] = data
    return HttpResponse(json.dumps(resp_dict, ensure_ascii=False, cls=Encoder))


class R(object):
    """
    统一项目信息返回结果类
    """

    def __init__(self):
        self.code = None
        self.msg = None
        self._data = dict()

    @staticmethod
    def ok():
        """
        组织成功响应信息
        :return:
        """
        r = R()
        r.code = StatusCodeEnum.OK.code
        r.msg = StatusCodeEnum.OK.msg
        return HttpResponse(json.dumps(r.data(), ensure_ascii=False))

    @staticmethod
    def login_fail():
        """
        登录失败响应信息
        :return:
        """
        r = R()
        r.code = StatusCodeEnum.LOGINFAIL.code
        r.msg = StatusCodeEnum.LOGINFAIL.msg
        return HttpResponse(json.dumps(r.data(), ensure_ascii=False))

    @staticmethod
    def error(msg=StatusCodeEnum.ERROR.msg):
        """
        组织错误响应信息
        :return:
        """
        r = R()
        r.code = StatusCodeEnum.ERROR.code
        r.msg = msg
        return r

    @staticmethod
    def server_error(msg=StatusCodeEnum.ERROR.msg):
        """
        组织服务器错误信息
        :return:
        """
        r = R()
        r.code = StatusCodeEnum.SERVER_ERR.code
        r.msg = msg
        return r.data()

    @staticmethod
    def set_result(enum):
        """
        组织对应枚举类的响应信息
        :param enum: 状态枚举类
        :return:
        """
        r = R()
        r.code = enum.code
        r.msg = enum.msg
        return r

    def data(self, key=None, obj=None):
        """统一后端返回的数据"""

        if key:
            self._data[key] = obj

        context = {
            'code': self.code,
            'msg': self.msg,
        }
        if self._data:
            context["data"] = self._data
        else:
            context["data"] = None
        return context
