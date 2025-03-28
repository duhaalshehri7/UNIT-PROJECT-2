from django.db import models

# Create your models here.

from users.models import DesignerPost,CustomUser


class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, "One Star"
        STAR2 = 2, "Two Stars"
        STAR3 = 3, "Three Stars"
        STAR4 = 4, "Four Stars"
        STAR5 = 5, "Five Stars"

    designer_post = models.ForeignKey(DesignerPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.STAR5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)





