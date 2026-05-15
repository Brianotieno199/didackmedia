from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


def optimize_image(image_field, max_width=1200, quality=75):
    if not image_field:
        return

    img = Image.open(image_field)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    width, height = img.size

    if width > max_width:
        new_height = int((max_width / width) * height)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=quality, optimize=True)

    file_name = os.path.splitext(image_field.name)[0] + ".webp"

    image_field.save(
        file_name,
        ContentFile(buffer.getvalue()),
        save=False
    )


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to='categories/')

    def save(self, *args, **kwargs):
        optimize_image(self.cover_image, max_width=1400, quality=75)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        optimize_image(self.image, max_width=1200, quality=75)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Photo"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        optimize_image(self.image, max_width=1200, quality=75)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    project_type = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.email}"