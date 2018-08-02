from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import  settings
from . import models
import hashlib,datetime
from .send_mail import send_mail
from .forms import UserForm,RegisterForm
# Create your views here.

def has_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = has_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def index(request):
    return render(request, 'login/index.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         message = "所有字段都必须填写！"
#         if username and password:
#             username = username.strip()
#             print(username, password)
#             try:
#                 user = models.User.objects.get(name=username)
#                 if user.password == password:
#                     return redirect('/login/index/')
#                 else:
#                     message = '密码不正确！'
#             except:
#                 message = '用户名不存在！'
#         return render(request, 'login/login.html', {'message': message})
#     return render(request, 'login/login.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = "请检查填写的内容!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '该用户未通过邮件确认'
                    return render(request, 'login/login.html', locals())
                if user.password == has_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/login/index/')
                else:
                    message = '密码不正确!'
            except:
                message = '用户不存在!'
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request,'login/login.html', locals())




def register(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写内容!"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['password1']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入密码不同!'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User()
                new_user.name = username
                new_user.password = has_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_mail(email, code)

                message = '请前往注册邮箱，进行邮件确认！'
                return render(request, 'login/confirm.html', locals())

    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/index/')
    request.session.flush()
    return redirect('/login/index/')

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录'
        return render(request, 'login/confirm.html', locals())