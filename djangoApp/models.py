#models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class TrainingLogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Date_Added = models.DateTimeField(auto_now_add=True, null=True)
    Training_Date=models.DateField(null=True)
    Techniques = models.CharField(max_length=100, null=True)
    Notes=models.TextField(blank=True, null=True)
    Duration = models.IntegerField(null=True, blank=True, help_text="Minutes")
    image = models.ImageField(upload_to='training_log_images/', blank=True, null=True)
    video = models.FileField(upload_to='training_log_videos/', blank=True, null=True)  # Video field added
    def __str__(self):
        return self.Training_Date.strftime('%Y-%m-%d') if self.Training_Date else 'Unknown Training Date'

class TechniqueLibraryEntry(models.Model):
    STATUS = (
        ('Needs Improvement', 'Needs Improvement'),
        ('Proficient', 'Proficient'),
        ('Mastered', 'Mastered'),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Technique_Name = models.CharField(max_length=200, null=True)
    Description = models.TextField(blank=True, null=True)
    Date_Added = models.DateTimeField(auto_now_add=True, null=True)
    Status = models.CharField(max_length=200, null=True, choices=STATUS)
    image = models.ImageField(upload_to='technique_library_images/', blank=True, null=True)
    video = models.FileField(upload_to='technique_library_videos/', blank=True, null=True)
    def __str__(self):
        return self.Technique_Name

class TechniqueSeriesEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    SeriesName = models.CharField(max_length=200, null=True)
    Description = models.TextField(blank=True, null=True)
    Techniques = models.ManyToManyField(
        'TechniqueLibraryEntry',
        through='TechniqueSeriesLinking',  
        blank=True
    )
    def __str__(self):
        return self.SeriesName
    

class TechniqueSeriesLinking(models.Model):
    TechniqueSeriesEntry = models.ForeignKey('TechniqueSeriesEntry', on_delete=models.CASCADE)
    TechniqueLibraryEntry = models.ForeignKey('TechniqueLibraryEntry', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('TechniqueSeriesEntry', 'TechniqueLibraryEntry')

    
