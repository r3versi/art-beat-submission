from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    mq = models.FloatField(default=0)

    
class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Paintings(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Camera(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now_add=True)


class CameraVisitors(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    visitors = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)


#######


class Word(models.Model):
    word = models.CharField(max_length=50)
    usages = models.IntegerField()
    lastused = models.DateTimeField(auto_now=True)

#####

class Feedback(models.Model):
    googleId = models.CharField(max_length=50, unique=True)
    datetime = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5)
    text = models.TextField(blank=True)
    confidence = models.FloatField(null=True)
    magnitude = models.FloatField(null=True, blank=True, default=None)
    score = models.FloatField(null=True, blank=True, default=None)

class Sentence(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    score = models.FloatField()
    magnitude = models.FloatField()

