from django.db import models

class Room(models.Model):
    description = models.TextField()


class Paintings(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Camera(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()


class CameraVisitors(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    visitors = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)


class RoomVisitors(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    visitors = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
