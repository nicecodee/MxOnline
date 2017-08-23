# encoding: utf8
__author__ = 'xuan'
__date__ = '2017/8/23 10:44'


'''导入python/django自带模块'''
from django import forms
import re   # 通过正则表达式，实现表单验证


'''导入第三方模块'''


'''导入自定义模块'''
from operations.models import UserAsk



'''自定义表单'''
# 除了继承django的forms.Form，我们还可以通过model转换成对应的form，以下就是例子

# “我要学习”表单, 用 UserAsk 这个Model直接转换而成
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk     # 指定需要转换成form的model
        fields = ['name', 'mobile', 'course_name']     # 选择指定model中特定的字段

    # 自定义表单验证（注：这类验证都是以 clean_ 开头）
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"    #通过正则表达式，验证手机号
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        raise forms.ValidationError(u"手机号码格式错误!", code="mobile_invalid")