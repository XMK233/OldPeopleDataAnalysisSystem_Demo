# coding=utf-8
from django.shortcuts import render

from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from .models import User
import os
import pdb
import time

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')


class UserFormLogin(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    checkcode = forms.CharField(label='VerificationCode')

def check_code(request):
    import io
    from .check_code import create_validate_code
    #import check_code as CheckCode
    stream = io.BytesIO()
    img, code = create_validate_code() #CheckCode.
    img.save(stream, "png")
    request.session['checkcode'] = code
    return HttpResponse(stream.getvalue(), "png")

def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            # 获取表单信息
            input_code = request.session['checkcode'].upper()
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            checkcode = uf.cleaned_data['checkcode'].upper()

            if input_code == checkcode:

                userResult = User.objects.filter(username=username, password=password)
                # pdb.set_trace()
                if (len(userResult) > 0):
                    response = render_to_response('SuccessLogin.html',
                                                  {'operation': "Log in", 'username': username},
                                                  context_instance=RequestContext(request))

                    response.set_cookie('username',username,60)
                    return response
                else:
                    #return HttpResponse("该用户不存在")
                    '''return render_to_response('register.html',
                                              {"errors": "User not exists"},
                                              context_instance=RequestContext(request))'''
            else:
                return render_to_response('register.html',
                                          {"errors": "Please enter the verification code"},
                                          context_instance=RequestContext(request))
    else:
        uf = UserFormLogin()


    return render_to_response("userlogin.html", {'uf': uf}, context_instance=RequestContext(request))


def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['username']
            # pdb.set_trace()
            # try:
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                return render_to_response('register.html',
                                          {"errors": "User exists"},
                                          context_instance=RequestContext(request))
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                errors = []
                if (password2 != password1):
                    errors.append("Password not the same")
                    return render_to_response('register.html',
                                              {'errors': errors},
                                              context_instance=RequestContext(request))
                    # return HttpResponse('两次输入的密码不一致!,请重新输入密码')
                password = password2
                email = uf.cleaned_data['email']
                # 将表单写入数据库
                user = User.objects.create(username=username, password=password1, email=email)
                # user = User(username=username,password=password,email=email)
                user.save()
                #pdb.set_trace()
                # 返回注册成功页面
                return render_to_response('SuccessRegister.html',
                                          {'username': username, 'operation': "Register"},
                                          context_instance=RequestContext(request))
    else:
        uf = UserForm()

    return render_to_response('Register.html', {'uf': uf}, context_instance=RequestContext(request))

def logout(request):
    nm = request.COOKIES.get('username')
    response = render_to_response('SuccessLogout.html',
                                  #{'username': nm},
                                  context_instance=RequestContext(request))
    #清理cookie里保存username
    response.delete_cookie('username')
    return response

@csrf_exempt
def upload(request):
    if request.method == "POST":
        file = request.FILES['file']
        #####################################3
        c = 0
        data = []
        label = []
        for chunk in file.readlines():
            line = str(chunk).replace("b\'", "").replace("\\r\\n\'", "").split(",")
            if c == 0:
                c += 1
                continue
            if c == 500:
                break
            c += 1
            if len(line) == 785:
                line = list(map(eval, line))
                data.append(line[1:])
                label.append(line[0])
        ##########################
        import requests, json
        test_data = {
            "instances": data
        }
        url = "http://scale05.eecs.yorku.ca:8501/v1/models/mnist_model:predict"
        r = requests.post(url, json=test_data)

        response = render_to_response('ResultDisplay.html',
                                      {'service': "sleeping condition",
                                       'result': json.loads(r.text)["predictions"],
                                       'label': label
                                       },#result
                                      context_instance=RequestContext(request))
        return response
    else:
        pass
    return render_to_response('UploadSlpCdtData.html')

def returnToList(request):
    if request.method == "POST":
        render_to_response("ServiceList.html")
    return render_to_response('ResultDisplay.html')

def goToServicePage(request):
    return render_to_response("ServiceList.html")

def sleepCondition(request):
    return render_to_response("SleepingCondition.html")