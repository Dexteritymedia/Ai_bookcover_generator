from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save,sender=User)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        profile = Profile.objects.create(user =instance)
