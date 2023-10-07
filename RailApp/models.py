from django.db import models

from django.db import models
# Create your models here.






class userregister(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=254)
    phone=models.IntegerField()
    age=models.IntegerField()
    addr=models.CharField(max_length=50)
    file=models.FileField()
    uname=models.CharField(max_length=20)
    pwd=models.CharField(max_length=20)
    forgot_pwd_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uname
    
from django.db import models

class Train(models.Model):
    name = models.CharField(max_length=100)
    # Other train fields
    def __str__(self):
        return self.name

class Station(models.Model):
    name = models.CharField(max_length=100)
    # Other station fields
    def __str__(self):
        return self.name

class Ticket(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    starting_station = models.ForeignKey(Station, related_name='starting_station', on_delete=models.CASCADE)
    destination_station = models.ForeignKey(Station, related_name='destination_station', on_delete=models.CASCADE)    
    ticket_price_inr = models.DecimalField(max_digits=8, decimal_places=2)
    train_time = models.DateTimeField(auto_now=False)
    ticket_name = models.CharField(max_length=100)
   

    # Other ticket fields
    def __str__(self):
        return self.ticket_name
    

class Booking(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    

    
    
    
 

 

    def __str__(self):
        return str(self.user)
    
    
    


# class Booking(models.Model):
#     user = models.ForeignKey(userregister, on_delete=models.CASCADE)
#     is_paid = models.BooleanField(default=False)
#     instamojo_id = models.CharField(max_length=1000)

class Customer(models.Model):
    cust_id=models.IntegerField()
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=100)



class Complaint(models.Model):
    user = models.ForeignKey(userregister,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    complaint = models.CharField(max_length=900)
    status = models.CharField(max_length=20)


class ComplaintAdmin(models.Model):
    date = models.DateField(auto_now=True)
    complaint = models.CharField(max_length=900)
    status = models.CharField(max_length=20)