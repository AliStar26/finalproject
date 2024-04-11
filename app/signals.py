from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Products, Category
import os

@receiver(pre_delete, sender=Products)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            print(f"Фото {instance.image.path}удален.")
        else:
            print(f"Фото {instance.image.path} не удален.")
    else:
        print("Нету фото")


@receiver(pre_delete, sender=Category)
def delete_category_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            print(f"Фото {instance.image.path}удален.")
        else:
            print(f"Фото {instance.image.path} не удален.")
    else:
        print("Нету фото")