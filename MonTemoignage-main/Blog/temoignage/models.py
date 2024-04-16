from django.db import models
from datetime import date
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
# Create your models here.



class Categorie(models.Model):
    cat_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.cat_name
    
class Article(models.Model):
    titre = models.CharField(max_length=255)
    nomAuteur = models.CharField(max_length=255)
    article = RichTextField()
    date = models.DateField(default=date.today)
    image = models.ImageField(default="", upload_to='images/')
    f_categorie = models.ForeignKey("Categorie", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class Video(models.Model):
    titre = models.CharField(max_length=255)
    nomAuteur = models.CharField(max_length=255)
    date = models.DateField(default=date.today)
    video = models.CharField(max_length=1000, null=True)
    # video = models.FileField(upload_to='videos/', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    image = models.ImageField(default="", upload_to='images/')
    f_categorie = models.ForeignKey("Categorie", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre
    
class Commentaire_Article(models.Model):
    nom = models.CharField(max_length=255)
    commentaire = RichTextField()
    date = models.DateField(default=date.today)
    f_article = models.ForeignKey("Article", related_name='comments', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.nom
    
class Commentaire_Video(models.Model):
    nom = models.CharField(max_length=255)
    commentaire = RichTextField()
    date = models.DateField(default=date.today)
    f_video = models.ForeignKey("Video", related_name='comments', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.nom
    

class Abonnee(models.Model):
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.email

    
class Team(models.Model):
    name = models.CharField(max_length=255)
    titre = models.CharField(max_length=255)
    description = RichTextField()
    image = models.ImageField(default="", upload_to='images/')
    
    def __str__(self):
        return self.name

    
@receiver(post_save, sender=Article)
@receiver(post_save, sender=Video)
def send_notification(sender, instance, created, **kwargs):
    if created:
        subscribers = Abonnee.objects.all()
        subject = "New Content Alert"
        message = "New content has been posted! Check it out: example.com"  # Replace example.com with your actual URL
        recipients = [subscriber.email for subscriber in subscribers]
        send_mail(subject, message, "your-email@example.com", recipients)
        
post_save.connect(send_notification, sender=Article)
post_save.connect(send_notification, sender=Video)