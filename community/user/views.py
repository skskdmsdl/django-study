from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Create your views here.

def home(request):
    user_id = request.session.get('user')

    if user_id:
        user = User.objects.get(pk=user_id)
        return HttpResponse(user.username)

    return HttpResponse('Home!')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}

        if not (username and password):
            res_data['error'] = '모든 값을 입력해야합니다!'
        else:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                # 비밀번호 일치. 로그인 처리됨
                # 세션
                request.session['user'] = user.id
                return redirect('/')
            else:
                res_data['error'] = '비밀번호를 틀렸습니다.'

        return render(request, 'login.html', res_data)

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None) # 기본값 지정(거짓을 의미하는 값 다 가능)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        # 유효성 검사는 front단에서 더 많이 하지만 back단에서 하는 방법도 있음
        res_data = {}

        if not (username and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다‼'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다!'
        else:
            # 클래스 변수 객체 생성(입력받은 값으로 객체 생성 -> DB에 저장)
            user = User(
                username=username,
                password=make_password(password) # 암호화
            )

            user.save()

        return render(request, 'register.html', res_data)