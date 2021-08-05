from django.urls import path

from . import views

app_name = 'financialApp'
urlpatterns = [
    path('users/', views.userIndexView.as_view(), name='user_index'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('transactions/', views.transaction_index, name='transaction_index'),
#    path('users/<int:user_id>/user_transaction_filtered', views.user_transaction_filtered, name='user_transaction_filtered')
]
