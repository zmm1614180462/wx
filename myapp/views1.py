from django.shortcuts import render
from django.core.cache import cache
from django.utils.timezone import now
import logging #使用日志
from django.views.decorators.cache import cache_page
import datetime
# Create your views here.
logger = logging.getLogger('myapp.views')
@cache_page(30)
def hello(request):
    return render(request, 'hello.html', {'time': now()})
    # try:
    #     # request.session['zmm'] = 'hello'
    #     # cache.set('cache', {'zmm': 1, 'zmm2': 2, 'zmm3': 3})
    #     # cache.set('zmm', {'zmm': 1, 'zmm2': 2, 'zmm3': 3})
    #     # print(cache.get('zmm'), cache.get('cache'))
    #     return render(request, 'hello.html', {'time': now()})
    # except Exception as e:
    #     logging.error(e)
def session(request):
    session = request.session.get('zmm')
    return render(request,'session.html',{'session':session})