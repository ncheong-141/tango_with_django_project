from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):

    maxlength_name = 128

    name = models.CharField(max_length=maxlength_name, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name

class Page(models.Model):

    maxlength_title = 128
    maxlength_url = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=maxlength_title)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
