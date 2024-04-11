from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class DateHolder(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, validators=[MinLengthValidator(10)], verbose_name='Number phone')
    birthday = models.DateField(verbose_name="Date of birth", null=True, blank=True)
    image = models.ImageField(upload_to='users/',verbose_name="Photo", default='users/default.jpg')



class Category(DateHolder):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category/',verbose_name="Photo", default='users/default.jpg')


    def __str__(self):
        return self.name

class Comment(DateHolder):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Products(DateHolder):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='products/',verbose_name="Photo", default='users/default.jpg')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category  = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    comments = models.OneToOneField(Comment, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    
    