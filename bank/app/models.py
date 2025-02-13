from django.db import models

# Create your models here.

class Gender(models.Model):
    gender = models.CharField(max_length=7)
    def __str__(self):
        return self.gender

class State(models.Model):
    state = models.CharField(max_length=50)
    def __str__(self):
        return self.state

class Account(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.PositiveBigIntegerField()
    acc_no = models.PositiveBigIntegerField(auto_created=True,unique=True)
    email = models.EmailField(unique=True)
    aadhar=models.PositiveBigIntegerField()
    father_name=models.CharField(max_length=50)
    dob = models.DateField()
    address = models.CharField(max_length=1000)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=500)
    pin = models.IntegerField(blank=True,default=0000)
    photo = models.ImageField(upload_to='profile_pics/')
    
    def save(self, *args, **kwargs):
        if not self.acc_no:
            last_acc = Account.objects.all().order_by('-acc_no').first()
            if last_acc:
                self.acc_no = last_acc.acc_no + 1
            else:
                self.acc_no = 1234567890
        super().save(*args, **kwargs)

