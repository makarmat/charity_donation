from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128)


INSTITUTIONS = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbióra lokalna')
)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTIONS, default=1)
    categories = models.ManyToManyField(Category, related_name='institution_category')


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='donation_category')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='donation_institution')
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_user', null=True, blank=True)
