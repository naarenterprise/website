from django.db import models
from django.utils.text import slugify


class HomeBanner(models.Model):
    title = models.CharField(max_length=200, blank=True, help_text="Optional label for admin reference.")
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(
        default=True,
        help_text="Only one banner should be active. The most recently updated active banner is shown.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Home banner"
        verbose_name_plural = "Home banners"

    def __str__(self):
        return self.title or f"Banner #{self.pk}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            HomeBanner.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)


class CaseStudy(models.Model):
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    tag = models.CharField(max_length=120, help_text="e.g. AUTOMOTIVE / ASSEMBLY")
    title = models.CharField(max_length=200)
    summary = models.TextField(help_text="Short description for the listing page.")
    image = models.ImageField(upload_to="case-studies/")
    challenge = models.TextField()
    solution = models.TextField()
    meta_inspection = models.CharField(max_length=120, blank=True)
    meta_integration = models.CharField(max_length=120, blank=True)
    meta_outcome = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "Case studies"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    quote = models.TextField()
    attribution = models.CharField(max_length=200, help_text="e.g. QUALITY HEAD / AUTOMOTIVE COMPONENTS")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return self.attribution


class Client(models.Model):
    category = models.CharField(max_length=80, help_text="e.g. AUTOMOTIVE")
    name = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Partner(models.Model):
    category = models.CharField(max_length=80, blank=True, help_text="e.g. TECHNOLOGY PARTNER")
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to="partners/", blank=True)
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
