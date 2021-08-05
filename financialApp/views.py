from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Transaction, User
from django.views import generic
from django.urls import reverse
import datetime
import json


class userIndexView(generic.ListView):
    template_name = 'financialApp/user_index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()

def user_detail(request, user_id):
    u = User.objects.get(id=user_id)
    t = None
    if request.method == 'POST':
        t = u.transaction_set.filter(date__range=[request.POST.get('start'), request.POST.get('end')])
        if request.POST.get('group')=='on': # if grouping is on, then we make a dict of dates -> sum amounts
            dict = {}
            for transaction in t.iterator():
                if transaction.date in dict:
                    dict[str(transaction.date)] = dict[str(transaction.date)] + float(transaction.amount);
                else:
                    dict[str(transaction.date)] = float(transaction.amount);
            json_string = json.dumps(dict) # create json from dict
            return render(request, 'financialApp/user_detail.html', {
                'user': u, 'transactions': t, 'grouped_amounts_json': json_string
                })
        else: # grouping is off, no json
            t = u.transaction_set.filter(date__range=[request.POST.get('start'), request.POST.get('end')])
            return render(request, 'financialApp/user_detail.html', {
                'user': u, 'transactions': t
                })
    else: # this is get, then return all transactions for this user
        t = u.transaction_set.all()
        return render(request, 'financialApp/user_detail.html',
            {'user' : u, 'transactions': t} )

def transaction_index(request):
    transaction_list = Transaction.objects.all()
    return render(request, 'financialApp/transaction_index.html', {'transaction_list' : transaction_list})
