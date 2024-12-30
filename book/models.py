from django.db import models

class Click(models.Model):
    stall_number = models.CharField(max_length=10, unique=True)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    description = models.TextField()
    events = models.TextField(null=True, blank=True)  # Allow NULL and blank values

    def __str__(self):
        return str(self.stall_number)
    
class Rectangle(models.Model):
    index = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"Rectangle {self.index}"
