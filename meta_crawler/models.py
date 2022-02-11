
from django.db import models


class Run(models.Model):
    timestamp = models.TimeField()


class Source(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="sources")
    type = models.CharField(max_length=100)
    path = models.CharField(max_length=1023)


class Owner(models.Model):
    name = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Meta(models.Model):
    location = models.CharField(max_length=1024)
    title = models.CharField(max_length=255)
    metadata = models.JSONField()
    owner_id = models.ForeignKey(Owner, on_delete=models.DO_NOTHING, related_name="metas")
    tags = models.ManyToManyField(Tag)
