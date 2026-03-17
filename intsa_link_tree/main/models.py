from django.db import models

class SiteConfig(models.Model):
    user_name = models.CharField(max_length=30)
    user_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    background_image = models.ImageField(upload_to='site/', blank=True, null=True)
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "SiteConfig":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class RedirectLink(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    logo_img = models.ImageField(upload_to='redirects/', blank=True, null=True)
    logo_svg = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)


class LinkClick(models.Model):
    LINK_TYPES = (
        ('redirect', 'Redirect Link'),
        ('product', 'Product Link'),
    )
    
    SOURCE_CHOICES = (
        ('instagram', 'Instagram'),
        ('other', 'Other'),
    )

    referer = models.URLField(blank=True, null=True)
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    link_type = models.CharField(max_length=20, choices=LINK_TYPES)
    link_id = models.IntegerField()

    def __str__(self):
        return f"{self.link_type} click at {self.timestamp}"


class ProductLink(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name