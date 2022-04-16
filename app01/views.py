from django.shortcuts import render, HttpResponse, redirect
from django import forms
from django.core.validators import RegexValidator

# Create your views here.


class MyForm(forms.Form):
    gender = forms.ChoiceField(
        choices=((1, '男'), (2, '女'), (3, '保密')),
        label='性别',
        initial=3,
        widget=forms.widgets.RadioSelect()
    )
    phone = forms.CharField(
        min_length=2,
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字')]
    )
    hobby = forms.MultipleChoiceField(
        choices=((1, '羽毛球'), (2, '篮球'), (3, '乒乓球')),
        label='爱好',
        initial=[1, 2],
        widget=forms.widgets.SelectMultiple()
    )
    hobby1 = forms.MultipleChoiceField(
        choices=((1, '羽毛球'), (2, '篮球'), (3, '乒乓球')),
        label='爱好',
        initial=[1, 2],
        widget=forms.widgets.CheckboxSelectMultiple()
    )
    keep = forms.ChoiceField(
        label='是否记住密码',
        initial='checked',
        widget=forms.widgets.CheckboxInput()
    )
    username = forms.CharField(
        min_length=4,
        max_length=8,
        widget=forms.widgets.TextInput(),
        error_messages={
            'min_length': '密码最少3位',
            'max_length': '密码最大8位',
            'required': "密码不能为空"
        }
    )


def forms(request):
    form_obj = MyForm()
    if request.method == "POST":
        form_obj = MyForm(request.POST)
        if form_obj.is_valid():
            return HttpResponse('OK')
    return render(request, 'forms.html', locals())


def set_cookie(request):
    res = render(request, 'set_cookie.html')
    res.set_cookie('username', 'wangsai', max_age=100)


def login_auth(func):
    def inner(request, *args, **kwargs):
        target_url = request.get_full_path()
        if request.COOKIES.get('username') == '123':
            return func(request, *args, **kwargs)
        else:
            return redirect('/login/?next={}'.format(target_url))
    return inner


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'wangsai' and password == '123':
            target_url = request.GET.get('next')
            print(target_url)
            if target_url:
                obj = redirect(target_url)
            else:
                obj = redirect('/home/')
            obj.set_cookie('username', '123')
            return obj
    return render(request, 'login.html', locals())

@login_auth
def home(request):
    # if request.COOKIES.get('username') == 'wangsai':
    #     return render(request, 'home.html')
    # return redirect('/login/')
    return render(request, 'home.html')


@login_auth
def index(request):
    return HttpResponse('我是index界面')


def logout(request):
    obj = redirect('/login/')
    obj.delete_cookie('username')
    return obj


from django.views import View
from django.utils.decorators import method_decorator


@method_decorator(login_auth, name='post')  # CBV添加装饰器的第二种方法
class MyLogin(View):
    @method_decorator(login_auth)                # CBV添加装饰器的第三种方法
    def dispatch(self, request, *args, **kwargs):
        pass

    @method_decorator(login_auth)      # CBV添加装饰器的第一种方法
    def get(self, request):
        return HttpResponse('你好啊')

    def post(self, request):
        return HttpResponse('我是post')


from django.contrib import auth


def login_superuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(request, username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
        else:
            return HttpResponse('账号或密码错误')
    return render(request, 'login_superuser.html')


from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/superuser')
def test(request):
    res = request.user.is_authenticated
    print(res)
    username = request.user
    print(username)
    return HttpResponse(res)


@login_required(login_url='/login/superuser')
def set_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not password == confirm_password:
            redirect('/set_password/')
        if not request.user.check_password(old_password):
            redirect('/set_password/')
        request.user.set_password(password)
        request.user.save()
    return render(request, 'home.html')


from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not password == confirm_password:
            redirect('/register/')
        User.objects.create_user(username=username, password=password)
        return HttpResponse('注册成功')
    return render(request, 'register.html')


@login_required(login_url='/login/superuser')
def out_log(request):
    auth.logout(request)