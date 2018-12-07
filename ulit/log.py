import os
from functools import wraps
import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

check_path = '.'
LOG_DIR = os.path.join(check_path, 'log')
file_stream = False
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
    file_stream = True

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.00"


def user_handler_log_formatter(record, handler):
    log = "[{dt}][{level}][{filename}][{func_name}][{lineno}] {msg}".format(
        dt=record.time,
        level=record.level_name,  # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=record.message,  # 日志内容
    )
    return log


# 打印到屏幕句柄
log_pout_handle = ColorizedStderrHandler(bubble=True)
log_pout_handle.formatter = user_handler_log_formatter

# 打印到文件句柄
log_pfile_handle = TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % 'monkey_log'), bubble=True)
log_pfile_handle.formatter = user_handler_log_formatter

# 用户代码logger日志
user_log = Logger("user_log")


def init_logger():
    logbook.set_datetime_format("local")
    user_log.handlers = []
    user_log.handlers.append(log_pout_handle)
    user_log.handlers.append(log_pfile_handle)


init_logger()


def logger(param):
    """ fcuntion from logger meta """

    def wrap(function):
        """ logger wrapper """

        @wraps(function)
        def _wrap(*args, **kwargs):
            """ wrap tool """
            user_log.info("当前模块 {}".format(param))
            user_log.info("全部args参数参数信息 , {}".format(str(args)))
            user_log.info("全部kwargs参数信息 , {}".format(str(kwargs)))
            return function(*args, **kwargs)

        return _wrap

    return wrap
