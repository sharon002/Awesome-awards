# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch  import receiver
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    bio = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        db_table = 'profile'

    @receiver(post_save, sender=User)
    def update_create_profile(sender,instance,created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)


    def save_profile(self):
        self.save()




class Projects(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='profile_pics/')
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    link = models.URLField()
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank = True, null=True)

    def save_project(self):
        self.save()

    def __str__(self):
        return f'{self.author} Post'

    class Meta:
        db_table = 'project'
        ordering = ['-created_date']

    def delete_project(self):
        self.delete()

    @classmethod
    def search_projects(cls, title):
        return cls.objects.filter(title__icontains=title).all()
        # return project

    @classmethod
    def get_project(cls,id):
        try:
            project = Projects.objects.get(pk=id)
            return project
        except ObjectDoesNotExist:
            raise Http404()
        