from django.db import models
from django.db.models import Avg
from django import template
register = template.Library()

from ..models import Book
from ...reviews.models import Review

@register.filter
def avg_ratings(self):
    avg = self.reviews.aggregate(models.Avg('rating'))
    if avg['rating__avg']:
        return int(round((avg['rating__avg'] * 20), -1))
    else:
        return 0