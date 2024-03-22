from django.contrib.auth.models import User
from .models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

@receiver(post_save, sender=User)
def UserProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email = user.email,
            name=user.first_name
            )
    else:
        profile = Profile.objects.get(user=instance)
        profile.username = instance.username
        profile.email = instance.email
        profile.name = instance.first_name
        profile.save()
        
    
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()