from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# ------------------------------------------------------
# USER MODEL
# ------------------------------------------------------

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("bd", "Bengali"),
]

ROLE_CHOICES = [
    ("admin", "Admin"),
    ("student", "Student"),
    ("teacher", "Teacher"),
    ("user", "User"),
]

class User(AbstractUser):
    handle = models.SlugField(max_length=30, unique=True, blank=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="en")
    last_active = models.DateTimeField(blank=True, null=True)

    # Optional: track when a user joined or last updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['email_verified']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_active']),
            models.Index(fields=['is_active', 'role']),
        ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Auto-generate unique handle (@username)
        if not self.handle:
            base = slugify(self.username)
            counter = 1
            unique_handle = f"@{base}"
            while User.objects.filter(handle=unique_handle).exists():
                unique_handle = f"@{base}{counter}"
                counter += 1
            self.handle = unique_handle
        super().save(*args, **kwargs)


# ------------------------------------------------------
# PROFILE MODEL
# ------------------------------------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="user_avatars/", default="user_avatars/default.jpg")

    # Learning / productivity fields
    bio = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    # System tracking
    joined_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# ------------------------------------------------------
# SIGNALS
# ------------------------------------------------------

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
