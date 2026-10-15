from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db import models

DAYS = [(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
        (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]


class Plan(models.Model):
    """One weekly timetable. Set once, followed for 7 days from start_date."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    start_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date', '-id']

    @property
    def end_date(self):
        return self.start_date + timedelta(days=6)

    def dates(self):
        return [self.start_date + timedelta(days=i) for i in range(7)]

    def __str__(self):
        return f'{self.user} {self.start_date} - {self.end_date}'


class Slot(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='slots')
    weekday = models.IntegerField(choices=DAYS)
    subject = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['weekday', 'start_time']

    @property
    def planned_minutes(self):
        return (self.end_time.hour * 60 + self.end_time.minute) - \
               (self.start_time.hour * 60 + self.start_time.minute)

    def __str__(self):
        return f'{self.subject} ({self.get_weekday_display()})'


class Log(models.Model):
    """Minutes actually studied for a slot on a particular date."""
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    minutes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('slot', 'date')
