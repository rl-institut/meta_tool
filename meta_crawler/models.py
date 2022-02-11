
from django.db import models


class Run(models.Model):
    timestamp = models.TimeField(auto_now=True)


class Source(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="sources")
    type = models.CharField(max_length=100)
    path = models.CharField(max_length=1023)


class Owner(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Meta(models.Model):
    source = models.ForeignKey(Source, on_delete=models.DO_NOTHING, related_name="metas")
    location = models.CharField(max_length=1024)
    version = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    metadata = models.JSONField()
    owner = models.ForeignKey(Owner, on_delete=models.DO_NOTHING, related_name="metas", null=True)
    tags = models.ManyToManyField(Tag)
