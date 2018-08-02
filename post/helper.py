from django.core.cache import cache

'''
更新策略
    主动更新
    主动删除
    过期时间
'''


def page_cache(timeout):
    def wrapper1(view_func):
        def wrapper2(request):
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            print('在缓存查找', response)
            if response is None:
                response = view_func(request)
                print('在数据库查找', response)
                cache.set(key, response, timeout)
                print('存储在缓存', response)
            return response
        return wrapper2
    return wrapper1
