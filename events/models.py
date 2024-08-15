from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Event.Status.PUBLISHED)
        )
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    class Timeline(models.TextChoices):
        EVENING = 'EV', 'Evening'
        MATINEE = 'MT', 'Matinee'
        NO_SERVICE = 'NS', 'No Service'
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='event_date'
    )
    presenter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    marquee = models.ImageField(
        upload_to="products/%Y/%m/%d",
        blank=True
    )
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        null=True,
        related_name='products',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    timeline = models.CharField(
        max_length=3,
        choices=Timeline,
        default=Timeline.EVENING
    )
    # publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['event_date']
        indexes = [
            models.Index(fields=['event_date']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'events:event_detail',
            args=[
                self.slug,
                self.event_date.year,
                self.event_date.month,
                self.event_date.day,
            ]
        )
    
    
    