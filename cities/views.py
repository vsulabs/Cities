from django.contrib import auth
from django.http import HttpResponseRedirect
from .game import *

def index(request):
    lvl = request.POST.get('lvl')
    if lvl is None:
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))

    request.session['lvl'] = lvl
    return HttpResponseRedirect("game")


def game(request):
    last = get_last(request)
    if len(last) == 0:
        return init(request)

    answer = request.POST.get('answer', '')
    name = last
    error = ''

    if answer != '':
        error_code = is_correct(request, answer)
        if error_code == 0:
            name = get_city(request, answer)
        else:
            error = get_error_message(error_code)

    template = loader.get_template('game.html')
    context = {
        'authenticated': request.user.is_authenticated(),
        'city': name,
        'error': error
    }

    return HttpResponse(template.render(context, request))


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    template = loader.get_template('login.html')
    if username == '' and password == '':
        return HttpResponse(template.render({}, request))

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        url = request.POST.get('referer')
        if url is None:
            url = '..'

        return HttpResponseRedirect(url)

    return HttpResponse(template.render({'error': True}, request))


def logout(request):
    auth.logout(request)
    url = request.POST.get('referer')
    if url is None:
        url = '..'

    return HttpResponseRedirect(url)


def reset(request):
    init(request)
    return HttpResponseRedirect("..")
