from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages_a', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages_a', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.CharField(max_length=250,blank=True, null=True)
    messages = models.ManyToManyField('Message', blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)
    country = CountryField(default='US')
    state = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?\d{1,15}$')], blank=True, null=True,)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Additional_Info(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to User model
    medical_history = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Additional Info'

    
