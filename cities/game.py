from django.shortcuts import render
from django.template import loader
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .models import City
from .storage import *
import ast

#TODO: session_key -> freq
frequency = {}     # char -> amount

for city in City.objects.all():
    if city.name == "":
        continue

    ch = city.name[0].lower()
    value = frequency.get(ch, 0)
    frequency[ch] = value + 1


def get_answered(request):
    answered = get_data(request, 'answered')
    if answered is None:
        return ['Москва']

    if isinstance(answered, list):
        return answered

    return ast.literal_eval(answered)


def get_last(request):
    return get_answered(request)[-1]


def get_key(city):
    ch = city.name[0].lower()
    return frequency.get(ch, 0)


def get_city(request, answer):
    last = answer[-1].upper()
    if last == 'Ь':
        last = answer[-2].upper()

    answered = get_answered(request)
    if answered is None:
        answered = []

    cities = City.objects.filter(name__startswith=last).all()
    cities = (c for c in cities if c.name not in answered)
    cities = sorted(cities, key=get_key)
    name = cities[0].name

    answered.append(answer)
    answered.append(name)
    set_data(request, 'answered', answered)

    return name


def is_correct(request, answer):
    answered = get_answered(request)

    if answer in answered:
        return 1

    all_cities = (c.name.lower() for c in City.objects.all())
    if answer.lower() not in all_cities:
        return 2

    last_word = answered[-1]
    last = last_word[-1]
    if last == 'ь':
        last = last_word[-2]

    if answer[0].lower() != last:
        return 3

    return 0


def get_error_message(error):
    return (
        '',
        'Такой город уже был',
        'Такого города нету',
        'Город должен начинаться на последнюю бувку предыдущего'
    )[error]


def init(request):
    template = loader.get_template('index.html')
    if not request.session.session_key:
        request.session.save()

    default_array = ['Москва']
    set_data(request, 'answered', default_array)
    data = {
        'authenticated': request.user.is_authenticated(),
        'city': default_array[-1],
        'error': ''
    }

    return HttpResponse(template.render(data, request))
