from django.db import models
import datetime

# Create your models here.
# Model for a new event
class Event_Profile(models.Model):
    content_area        = models.CharField(max_length=120) #max_length = required
    event_date          = models.DateField(default=datetime.date.today) # Need to make this more flexible
    event_location      = models.CharField(max_length=120)
    workshop_number     = models.CharField(max_length=15)
    cost_per_person     = models.DecimalField(max_digits=10,decimal_places=2)
    #def __str__(self):
        #return self.name

# Create an attendance listing for an existing event
class Attendance_Entry(models.Model):
    event_id            = models.PositiveIntegerField()
    district_name       = models.CharField(max_length=120)
    number_registered   = models.PositiveIntegerField()
    number_of_noshows   = models.PositiveIntegerField()
    #def __str__(self):
        #return self.name

# Table that can be used as a ModelChoiceField to set the content_area value
class Content_Area(models.Model):
    content_name        = models.CharField(max_length=120)
    def __str__(self):
        return self.content_name

# Table that can be used as a ModelChoiceField to set the district_name value
class District(models.Model):
    district_name       = models.CharField(max_length=120)
    def __str__(self):
        return self.district_name
