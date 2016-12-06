from .models import AccountData


def get_data(request, key):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            record = AccountData.objects.get(username=username, key=key)
            return record.value
        except:
            return None
    else:
        if key in request.session.keys():
            return request.session[key]
        else:
            return None


def set_data(request, key, value):
    if request.user.is_authenticated():
        username = request.user.username
        try:
            record = AccountData.objects.get(username=username, key=key)
            record.value = value
            record.save()
        except AccountData.DoesNotExist:
            record = AccountData(username=username, key=key, value=str(value))
            record.save()
    else:
        request.session[key] = value


def delete_data(request, key):
    if request.user.is_authenticated():
        username = request.user.username
        AccountData.objects.filter(username=username).filter(key=key).delete()
    else:
        del request.session[key]
