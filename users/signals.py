from django.db.models.signals import post_save

from django.dispatch import receiver

from django.contrib.auth.models import User

from users.models import Profile, UserCustom


"""
We need to create Profile Each time new User add, so a signal created so when new User added
@receiver will receive a signal from it and create new Profile created with User as ForeignKey.
"""
@receiver(post_save, sender=UserCustom)

def create_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()