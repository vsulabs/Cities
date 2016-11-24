from django.shortcuts import render
from django.template import loader
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .game import is_correct, get_city, get_error_message, init, get_last
from .game import login_user

def index(request):
  key = request.session.session_key
  last = get_last(key)
  if last == '':
    return init(request)
  
  answer = request.GET.get('answer', '')
  name = get_last(key)
  error = ''

  if answer != '':
    error_code = is_correct(key, answer)
    if error_code == 0:
      print("get_city")
      name = get_city(key, answer)
    else:
      error = get_error_message(error_code)

  print(name)
  template = loader.get_template('index.html')
  context = {
    'authorized': request.user.is_authenticated(),
    'city': name,
    'error': error
  }

  return HttpResponse(template.render(context, request))


def login(request):
  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  template = loader.get_template('login.html')
  if (username == '' and password == ''):
    return HttpResponse(template.render({}, request))

  user = auth.authenticate(username=username, password=password)
  key = request.session.session_id
  if user is not None and user.is_active:
    auth.login(request, user)
    login_user(username, key)
    return HttpResponseRedirect("..")

  return HttpResponse(template.render({'error': True}, request))

def logout(request):
  auth.logout(request)
  return HttpResponseRedirect("..")
