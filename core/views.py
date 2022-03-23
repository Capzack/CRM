from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render

from core.models import Lid, Deal, Sell

Channel = {
    'site': 'Сайт', 'phone': 'Телефон', 'social': 'Социальные сети', 'email': 'Електронная почта'
}
Status ={
    'New': 'Новый', 'Kvali': 'Квалификация', 'Defeat': 'Проигрышный статус', 'Deal': 'В сделке'}
DealStatus ={
    'New': 'Новый', 'Interes': 'Выяснение интереса', 'Chek': 'Проверка закупки ', 'Offer':'Rоммерческое предложение', 'Done': 'Завершенна'
}

def lidsByChannel(request):
    res = Lid.objects.all().values('Channel').annotate(Count('Name'))
    for i in res:
        i['Name'] = Channel[i['Channel']]
    print(res)
    return render(request, 'lidsByChannel.html', {'res': res})

def Conversion(request):
    lids = Lid.objects.all().values('Manager').annotate(Count('Manager'))
    for i in lids:
        i['Name'] = User.objects.get(id=i['Manager'])
        i['Deal'] = Deal.objects.all().filter(Manager=i['Manager']).count()
        i['Conv'] = i['Deal'] / i['Manager__count']  * 100
    print(lids)
    return render(request, 'Conversion.html', {'lids': lids})

def ConversionDeal(request):
    deal = Deal.objects.all().values('Manager').annotate(Count('Manager'))
    for i in deal:
        i['Name'] = User.objects.get(id=i['Manager'])
        i['Sell'] = Sell.objects.all().filter(Manager=i['Manager']).count()
        i['Conv'] = i['Sell'] / i['Manager__count'] * 100
    print(deal)
    return render(request, 'ConversionDeal.html', {'deal': deal})

def lidsByStatus(request):
    res = Lid.objects.all().values('Status').annotate(Count('Name'))
    for i in res:
        i['Name'] = Status[i['Status']]
    print(res)
    return render(request, 'lidsByStatus.html', {'res': res})

def DealByStatus(request):
    res = Deal.objects.all().values('Status').annotate(Count('Sum'))
    for i in res:
        i['Name'] = DealStatus[i['Status']]
    print(res)
    return render(request, 'DealByStatus.html', {'res': res})