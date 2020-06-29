# from DOCS, post_save triggered once data saved at DB
# so we need it when new User added
from django.db.models.signals import post_save

# receiver decorator function that will receive this signal
from django.dispatch import receiver

from django.contrib.auth.models import User

from users.models import Profile

# post_save will be triggered each time new item added to DB
# but we need it just when new User created, so we define sender=User for that.
# so receiver function will never run unless the sender is User model
@receiver(post_save, sender=User)

# function that will run when @receiver runs
# post_save from DOCS came with 4 variables that we define inside this function
# and depending on them we create new Profile and attach it with its User
def create_save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()