from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .library import Library


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Library, related_name="librarians",
        null=True, # Makes column nullable in DB
        blank=True, # Allows blank value on objects
        on_delete=models.CASCADE)


# These receiver hooks allow you to continue to
# work with the `User` class in your Python code.


# Every time a `User` is created, a matching `Librarian`
# object will be created and attached as a one-to-one
# property
@receiver(post_save, sender=User)
def create_librarian(sender, instance, created, **kwargs):
    if created:
        Librarian.objects.create(user=instance)

# Every time a `User` is saved, its matching `Librarian`
# object will be saved.
@receiver(post_save, sender=User)
def save_librarian(sender, instance, **kwargs):
    instance.librarian.save()