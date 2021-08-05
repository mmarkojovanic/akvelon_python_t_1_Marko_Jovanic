from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    def __str__(self):
        return self.first_name + ' '+self.last_name

class Transaction(models.Model):
    date = models.DateField('time of transaction')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=10, max_digits=20)
    def __str__(self):
        return 'User: '+ self.user.first_name+' '+self.user.last_name +', amount: '+str(self.amount) + ' , date: ' + str(self.date)
