from django.db import models
from django.conf import settings
#from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from django.core.files import File
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

from PIL import Image

User = get_user_model()

# Create your models here.

class HomePage(models.Model):
    book_cover = models.ImageField(upload_to='home', null=True, blank=True)
    prompt = models.TextField()
    cover_num = models.PositiveIntegerField()

    def __str__(self):
        return self.id

    def book_cover_img(self):
        if self.book_cover:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" /.>' %(self.book_cover)
                )
        return None

    def save(self, *args, **kwargs):
        import urllib, os
        #from urlparse import urlparse

        file_save_dir = 'home'
        print(file_save_dir)
        url = 'https://replicate.delivery/mgxm/59d9390c-b415-47e0-a907-f81b0d9920f1/187400315-87a90ac9-d231-45d6-b377-38702bd1838f.jpg'
        #filename = urlparse(url).path.split('/')[-1]
        #result = urllib.request.urlretrieve(url)
        #self.book_cover = os.path.join('home', filename)
        #File(open(result[0], 'rb'))
        #result = urllib.urlretrieve(url, os.path.join(file_save_dir))
        #self.book_cover = os.path.join(file_save_dir, File(open(result[0], 'rb')))
        result = urllib.request.urlretrieve(url)
        print(result)
        self.book_cover.save(os.path.basename(url), File(open(result[0], 'rb')))
        #self.save()
        super(HomePage, self).save(*args, **kwargs)

        
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
        img.save(self.image.path)
    

class Payment(models.Model):
    PLAN = (
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    )
    amount = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=100, choices=PLAN, null=True, blank=True)
    description = models.TextField(blank=True)
    credit = models.PositiveIntegerField(default=25)

    def __str__(self):
        return str(self.plan)


class CustomerPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    amount = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=False)
    payment_credit = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.status} {self.date}"

class CoverGenerator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='users', blank=True)
    prompt = models.TextField()
    slug = models.SlugField(max_length=200, null=True, blank=True)
    resized_cover = models.ImageField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user.username:
            try:
                return self.user.username
            except AttributeError:
                return 'Anonymous'

    @property
    def cover_url(self):
        try:
            url = self.cover.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.prompt)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cover-generator", kwargs={"slug": self.slug})
        
    


