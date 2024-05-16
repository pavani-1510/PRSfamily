from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title

# models.py

from django.db import models

class FamilyMember(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
