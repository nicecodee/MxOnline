# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/26 12:33'


'''导入python/django自带模块'''
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


'''导入第三方模块'''

'''导入自定义模块'''



'''自定义类'''
class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
