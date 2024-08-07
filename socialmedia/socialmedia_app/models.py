from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20,
                              choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')],
                              default='pending')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user}-{self.to_user}"


@receiver(post_save, sender=FriendRequest)
def create_friend_after_acceptance(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return

    if instance.status == 'accepted':
        if not Friend.objects.filter(user=instance.from_user, friend=instance.to_user).exists():
            Friend.objects.create(user=instance.from_user, friend=instance.to_user)

        if not Friend.objects.filter(user=instance.to_user, friend=instance.from_user).exists():
            Friend.objects.create(user=instance.to_user, friend=instance.from_user)


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friend_of', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user}-{self.friend}"
