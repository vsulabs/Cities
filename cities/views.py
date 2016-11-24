from django.shortcuts import render
from django.template import loader
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .game import is_correct, get_city, get_error_message, init

def index(request):
  if not request.session.session_key:
    return init(request)
  
  last = request.session.get('last_step', '')
  answer = request.GET.get('answer', '')
  name = last
  error = ''
  answered = request.session.get('answered', set()) 
  key = request.session.session_key

  if answer != '':
    error_code = is_correct(key, answer)
    if error_code == 0:
      name = get_city(key, answer)
    else:
      error = get_error_message(error_code)

  print('"' + name + '"')
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
  if user is not None and user.is_active:
    auth.login(request, user)
    return HttpResponseRedirect("..")

  return HttpResponse(template.render({'error': True}, request))

def logout(request):
  auth.logout(request)
  return HttpResponseRedirect("..")
