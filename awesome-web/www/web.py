'''
web的http方法
'''
import functools, asyncio, inspect, logging, os

# GET
def get(path):
    # 装饰器
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

# POST
def post(path):
    # 装饰器
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

'''
RequestHandler
- Descript: 从URL函数中分析需要接受的参数，并从request中获取参数
'''
class RequestHandler:

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    async def __call__(self, request):
        r = await self._func()
        return r

# 注册一个URL处理函数
def add_route(app, fn):
    method = getattr(fn, '__method__')
    path = getattr(fn, '__route__')

    if path is None or method is None:
        raise ValueError('@get or @posth not defined in %s.' % str(fn))

    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s => %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.route.add_route(method, path, RequestHandler(app, fn))

# 自动扫描
def add_routes(app, module_name):
    n = module_name.rfind(',')
    if n == -1:
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1 :]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__')
            path = getattr(fn, '__route__')
            if method and path:
                add_route(app, fn)

def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))
    
