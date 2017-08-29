from __future__ import unicode_literals
from ..login.models import User
from django.db import models
import datetime

class TripManager(models.Manager):
    def validate_trip(self, postData, user_id):
        errors = {}
        for field, value in postData.iteritems():
            if len(value) < 1:
                errors[field] = 'All Fields are Required'
        if postData['start'] <= datetime.date.today().strftime('%Y-%m-%d'):
            errors['start'] = 'Trip must start in the future'
        if postData['end'] <= postData['start']:
            errors['end'] = 'Trip must end after start date'
        if len(errors) == 0:
            self.create(
                dest = postData['dest'],
                desc = postData['desc'],
                start = postData['start'],
                end = postData['end'],
                planner = User.objects.get(id=user_id)
            )
        else:
            return errors

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    desc = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    planner = models.ForeignKey(User, related_name='trips')
    joiners = models.ManyToManyField(User, blank=True, null=True)
    objects = TripManager()
    def __repr__(self):
        return 'Trip Planned for {} by {}'.format(self.dest, self.planner.name)
