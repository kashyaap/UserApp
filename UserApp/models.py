from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserDetail(models.Model):
    """
    Extends user details by linking with Django's User model. 
    Handles additional fields like phone_number and bio.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)

    class Meta:
        unique_together = ('phone_number', 'email')  # Ensure unique combination

    def __str__(self):
        return f"{self.user.username}'s Details"

    def save(self, *args, **kwargs):
        """
        Sync username and email from the User model on save.
        """
        self.username = self.user.username
        self.email = self.user.email
        super().save(*args, **kwargs)

    @staticmethod
    def find_common_users(phone_number, email):
        """
        Returns users with the same phone number or email.
        """
        return UserDetail.objects.filter(
            Q(phone_number=phone_number) | Q(email=email)
        ).distinct()

@receiver(post_save, sender=User)
def create_or_update_user_detail(sender, instance, created, **kwargs):
    """
    Automatically creates or updates the UserDetail when a User instance is saved.
    Prevents duplicate UserDetail creation by checking if it exists.
    """
    if created:
        # Only create UserDetail if it doesn't already exist
        UserDetail.objects.get_or_create(user=instance)
    else:
        # Update the existing UserDetail if user is updated
        instance.userdetail.save()

