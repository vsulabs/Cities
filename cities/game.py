from django.shortcuts import render
from django.template import loader
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .models import City

frequency = {}

def get_key(city):
  ch = city.name[0].lower()
  return frequency.get(ch, 0)


def get_city(answered, answer):
  last = answer[-1].upper()
  if (last in {'Ь'}):
    last = answer[-2].upper()

  cities = City.objects.filter(name__startswith=last).all()
  cities = (c for c in cities if c.name not in answered)
  cities = sorted(cities, key=get_key)
  return cities[0].name

def is_correct(context, answer):
  answered = context.get('answered', {})
  if (answer in answered):
    return 1

  all_cities = (c.name.lower() for c in City.objects.all())
  if (answer.lower() not in all_cities):
    return 2

  last_step = context.get('last_step', '').lower()
  last = last_step[-1]
  if (last in {'ь'}):
    last = last_step[-2]

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
  for city in City.objects.all():
    if city.name == "":
      continue;

    ch = city.name[0].lower()
    value = frequency.get(ch, 0)
    frequency[ch] = value + 1;

  template = loader.get_template('index.html')
  request.session['last_step'] = 'Москва'
  request.session['answered'] = []
  data = {
    'city': request.session['last_step'],
    'error': ''
  }

  return HttpResponse(template.render(data, request))
