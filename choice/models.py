from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone
# -*- coding:utf-8 mode:python -*-

# Create your models here.
MY_CHOICES = (('item_key1', 'Item title 1.1'),
              ('item_key2', 'Item title 1.2'),
              ('item_key3', 'Item title 1.3'),
              ('item_key4', 'Item title 1.4'),
              ('item_key5', 'Item title 1.5'))

MY_CHOICES2 = ((1, 'Item title 2.1'),
               (2, 'Item title 2.2'),
               (3, 'Item title 2.3'),
               (4, 'Item title 2.4'),
               (5, 'Item title 2.5'))


class MyExam(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class MyChoice(models.Model):
    exam = models.ForeignKey('MyExam', on_delete=models.CASCADE)
    no = models.IntegerField(default=0)
    my_choice = MultiSelectField(choices=MY_CHOICES2,max_choices=1, max_length=6)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.my_choice
    

class MyModel(models.Model):

    my_field = MultiSelectField(choices=MY_CHOICES)
    my_field2 = MultiSelectField(choices=MY_CHOICES2,
                                 max_choices=3,
                                 max_length=3)
