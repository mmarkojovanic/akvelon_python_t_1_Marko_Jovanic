from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Transaction, User
from django.views import generic
from django.urls import reverse
import datetime
import json


def user_index(request):
    if(request.method == 'POST'):
        sort = request.POST.get('sort')
        name_substring = request.POST.get('name_text') # check wheather first or last name contains given string
        u = User.objects.filter(first_name__icontains=name_substring).union(
            User.objects.filter(last_name__icontains=name_substring))
        if(sort == 'first_name'): # if needs to be sorted by first_name
            u = u.order_by('-first_name')
        elif(sort == 'last_name'):
            u = u.order_by('-last_name')
    else:
        u = User.objects.all()
    return render(request, 'financialApp/user_index.html', {'user_list':u} )



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
    if(request.method == 'POST'):
        income_outcome = request.POST.get('income_outcome')
        sort = request.POST.get('sort')
        if(income_outcome=='income'): # check if user needs only income or outcome transactions
            transaction_list = Transaction.objects.filter(amount__gte=0).filter(date__range=
            [request.POST.get('start'), request.POST.get('end')])
        elif(income_outcome=='outcome'):
            transaction_list = Transaction.objects.filter(amount__lte=0).filter(date__range=
            [request.POST.get('start'), request.POST.get('end')])
        else:
            transaction_list = Transaction.objects.filter(date__range=
                        [request.POST.get('start'), request.POST.get('end')])
        if(sort == 'amount'): # check if transactions need to be sorted
            transaction_list = transaction_list.order_by('-amount')
        elif(sort == 'date'):
            transaction_list = transaction_list.order_by('-date')
    else:
        transaction_list = Transaction.objects.all()
    return render(request, 'financialApp/transaction_index.html', {'transaction_list' : transaction_list})
