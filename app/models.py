from django.db import models
from django.utils import timezone
# from djgeojson.fields import  PointField


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=True)
    categories = models.ManyToManyField('app.Category')

    def __str__(self):
        return self.title

    @property
    def days_since_creation(self):  # can also be declared in admin, see "edited_today"
        diff = timezone.now() - self.date_created
        return diff.days


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        # verbose_name = 'Category'


class Place(models.Model):
    pass
    # for Windows:
    # https://stackoverflow.com/questions/49139044/geodjango-on-windows-could-not-find-the-gdal-library-oserror-winerror-12

    # name = models.CharField(max_length=255)
    # location = PointField()
    #
    # def __str__(self):
    #     return self.name
