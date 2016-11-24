from django.shortcuts import render
from django.template import loader
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from .models import City

frequency = {} # char -> amount
answered = {} # session_key -> set()
last_step = {} # session_key -> string

def get_last(key):
  return last_step[key]

def get_key(city):
  ch = city.name[0].lower()
  return frequency.get(ch, 0)


def get_city(key, answer):
  last = answer[-1].upper()
  if (last in {'Ь'}):
    last = answer[-2].upper()

  cities = City.objects.filter(name__startswith=last).all()
  cities = (c for c in cities if c.name not in answered[key])
  cities = sorted(cities, key=get_key)
  name = cities[0].name

  answered[key].add(answer)
  answered[key].add(name)
  last_step[key] = name

  return name

def is_correct(key, answer):
  if (answer in answered[key]):
    return 1

  all_cities = (c.name.lower() for c in City.objects.all())
  if (answer.lower() not in all_cities):
    return 2

  last = last_step[key][-1]
  if (last == 'ь'):
    last = last_step[key][-2]

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
  if not request.session.session_key:
      request.session.save()

  key = request.session.session_key
  last_step[key] = 'Москва'
  answered[key] = set()
  print("inited: " + key)
  data = {
    'city': last_step[key],
    'error': ''
  }

  return HttpResponse(template.render(data, request))
