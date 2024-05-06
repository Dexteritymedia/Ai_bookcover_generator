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
        return str(self.id)

    def book_cover_img(self):
        if self.book_cover:
            return mark_safe(
                '<img src="/media/%s" width="50" height="50" /.>' %(self.book_cover)
                )
        return None

    def save(self, *args, **kwargs):
        import urllib, os
        
        url = 'https://replicate.delivery/mgxm/59d9390c-b415-47e0-a907-f81b0d9920f1/187400315-87a90ac9-d231-45d6-b377-38702bd1838f.jpg'
        result = urllib.request.urlretrieve(url)
        self.book_cover.save(os.path.basename(url), File(open(result[0], 'rb')), save=False)
        super(HomePage, self).save(*args, **kwargs)


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    question_no = models.PositiveIntegerField()

    def __str__(self):
        return self.question

        
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

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
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date_added = models.DateTimeField(auto_now=True)
    plan = models.CharField(max_length=100, choices=PLAN, null=True, blank=True)
    description = models.TextField(blank=True)
    credit = models.PositiveIntegerField(default=25)

    def __str__(self):
        return str(self.plan)

    def get_payment_features(self):
        return self.payment_plan.all()

class PaymentFeature(models.Model):
    feature = models.CharField(max_length=150)
    payment = models.ManyToManyField(Payment, default=None, blank=True, related_name="payment_plan")
    #payment = models.ForeignKey(Payment, default=None, on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_plan")

    def __str__(self):
        return self.feature

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


class ImageEditing(models.Model):

    ROBOTO = 'Roboto'
    ZCOOL = 'ZCOOL'
    FONT_CHOICES = (
        (ROBOTO, 'Roboto'),
        (ZCOOL, 'ZCOOL'),
    )

    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images-edit/')
    blank = models.ImageField(upload_to='images-edits/blanks/')

    image = models.ForeignKey(
        CoverGenerator,
        related_name='images',
        on_delete=models.DO_NOTHING,
    )
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    font = models.CharField(
        max_length=100,
        choices=FONT_CHOICES,
        default=ROBOTO,
    )

    size = models.IntegerField(default=10)
    color = models.CharField(max_length=100)

    alt_text = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
        
    


