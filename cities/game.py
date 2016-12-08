from django.template import loader
from django.http import HttpResponse
from random import random
import ast
from .models import City
from .storage import *


def get_answered(request):
    answered = get_data(request, 'answered')
    if answered is None:
        return []

    if isinstance(answered, list):
        return answered

    return ast.literal_eval(answered)


def get_last(request):
    answered = get_answered(request)
    if len(answered) == 0:
        return ''

    return answered[-1]


def get_comparator(request):
    frequency = get_data(request, 'frequency')
    if isinstance(frequency, str):
        frequency = ast.literal_eval(frequency)

    def get_key(city):
        char = city.name[0].lower()
        return frequency.get(char, 0)

    return get_key


def get_city(request, answer):
    last = answer[-1].upper()
    if last == 'Ь':
        last = answer[-2].upper()

    answered = get_answered(request)
    cities = City.objects.filter(name__startswith=last).all()
    cities = (c for c in cities if c.name not in answered and c.name[0] == last)

    lvl = request.session.get('lvl')
    if lvl is None or lvl == 'easy':
        cities = list(cities)
        i = round(random() * len(cities))
        name = cities[i].name
    else:
        cities = sorted(cities, key=get_comparator(request))
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


def init_freq(request):
    frequency = {}  # char -> amount
    for city in City.objects.all():
        if city.name == "":
            continue

        ch = city.name[0].lower()
        value = frequency.get(ch, 0)
        frequency[ch] = value + 1

    set_data(request, 'frequency', frequency)


def init(request):
    template = loader.get_template('index.html')

    init_freq(request)
    default_array = ['Москва']
    set_data(request, 'answered', default_array)
    data = {
        'authenticated': request.user.is_authenticated(),
        'city': default_array[-1],
        'error': ''
    }

    return HttpResponse(template.render(data, request))
