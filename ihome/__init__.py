from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import redis
from config import config_map

"""
一. 这个init文件主要向外暴露两方面的内容:
    1. create_app, 创建应用的工厂方法, 里面封装创建应用的具体逻辑
    2. 其他文件需要引入的一些扩展对象, 如db, redis_connect等

二. flask扩展插件有两种初始化方式, 以flask_sqlalchemy为例:
    1. 创建db对象的同时传入app对象: 
        db.SQLAlechmy(app)
        即先创建app, 再创建扩展对象
    2. 创建db对象时不传入appd对象, 等到app对象创建出来后再调用db对象的init_app将app绑定
        db.SQLAlchemy()
        ...
        db.init_app(app)
        即先创建扩展对象, 再在创建app时将扩展对象与app绑定, 延迟绑定
    对于那些需要放在create_app外面的扩展对象, 就需要使用第二种方法, 即先创建, 后绑定app
    
三. 对于redis连接这种不属于flask扩展插件的对象, 可以先定义一个全局变量, 初始化为None
    在create_app的方法中再赋予具体的对象值, 也能达到延迟绑定的效果

四. 对于Session和CSRFProtect初始化的对象并不需要暴露在外面, 因为这两个对象只是赋予
    或者修改了一些app的机制, 后续程序使用时并不会调用这两个对象
"""

# 创建数据库链接
db = SQLAlchemy()
# 初始化redis连接
redis_connect = None


# 创建应用工厂
def create_app(env):
    """
    创建app的工厂方法
    :param env: str 环境参数 ('dev'/'prod')
    :return: app
    """
    app = Flask(__name__)
    # 应用添加配置
    config_class = config_map.get(env)
    app.config.from_object(config_class)

    # 绑定flask扩展
    # 初始化绑定mysql数据库
    db.init_app(app)
    # 创建redis连接
    global redis_connect
    redis_connect = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT,
                                      db=config_class.REDIS_CACHE_DB)
    # 将session绑定为app中的设置
    Session(app)
    # 启用CSRF模块
    CSRFProtect(app)

    # 注册蓝图, 蓝图最好是注册前才导入
    from ihome.api_1_0 import api
    app.register_blueprint(api)
    return app
