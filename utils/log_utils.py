import time
from loguru import logger
from pathlib import Path

# 获取当前文件路径的父目录
project_path = Path.cwd()
log_path = Path(project_path, "log")
t = time.strftime("%Y_%m_%d")
print(log_path)


class Loggings:
    __instance = None
    logger.add("%s/interface_log_%s.log" % (log_path, t), rotation="500MB", encoding="utf-8", enqueue=True,
               retention="10 days")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def info(self, msg):
        return logger.info(msg)

    def debug(self, msg):
        return logger.debug(msg)

    def warning(self, msg):
        return logger.warning(msg)

    def error(self, msg):
        return logger.error(msg)


loggings = Loggings()
