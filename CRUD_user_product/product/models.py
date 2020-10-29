from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
from cms.models.pluginmodel import CMSPlugin
# from aldryn_bootstrap3 import model_fields
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    birthdate = models.DateField()
    city = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True, blank=False)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.firstname + ' ' + self.lastname


class Product(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=50)
    product_type = models.CharField(max_length=50)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.product_name




class Hello(CMSPlugin):
    guest_name = models.CharField(max_length=50, default='Guest')


class Menu_Item(CMSPlugin):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="menu_items")
    price = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s" % (self.name,)

class Employee(CMSPlugin):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self):
        return "%s" % (self.fname,)


# class UserCustom_Plugin(CMSPlugin):
#     fname = models.CharField(max_length=200)
#     items_per_page = models.PositiveIntegerField(
#         verbose_name= _('Items per page'),
#         null=False,
#         blank=False,
#         help_text= _('Show number of items per page'),
#     )
#
#     def __str__(self):
#         return str(self.items_per_page)

class User_Custom_Plugin(CMSPlugin):
    items_per_page = models.PositiveIntegerField(
        verbose_name= _('Items per page'),
        null=False,
        blank=False,
        help_text= _('Show number of items per page'),
        default=0
    )

    def __str__(self):
        return str(self.items_per_page)

