
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_designer = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )


    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )


class DesignerProfile(models.Model):
    class Specialty(models.TextChoices):
        UX_UI = "UX/UI Design"
        LOGO_BRANDING = "Logo & Branding Design"
        WEB_APP = "Web & App Design"
        VIDEO_MOTION = "Video & Motion Graphics"
        PRODUCT_INDUSTRIAL = "Product & Industrial Design"

    class ExperienceLevel(models.TextChoices):
        BEGINNER = "Beginner"
        INTERMEDIATE = "Intermediate"
        EXPERT = "Expert"

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50, choices=Specialty.choices)
    experience = models.TextField()
    location = models.CharField(max_length=255)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.INTERMEDIATE)
    pricing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.specialty}"

class DesignerPost(models.Model):
    designer = models.OneToOneField(DesignerProfile, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to="profile_photos", default="img/default_user.jpg")
    about_me = models.TextField()
    availability = models.BooleanField(default=False)
    contact_email = models.EmailField()
    portfolio_url = models.URLField(blank=True, null=True)

    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.designer} - {self.profile_photo}"




class DesignerPostImage(models.Model):
    designer_post = models.ForeignKey(DesignerPost, on_delete=models.CASCADE, related_name="work_samples")
    image = models.ImageField(upload_to="work_samples")
    def __str__(self):
        return f"{self.designer_post} - {self.image}"


class Bookmark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    designer_post = models.ForeignKey(DesignerPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

