from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=128, blank=False)
    date = models.DateTimeField(blank=False, db_index=True)
    description = models.TextField(blank=False)
    participants = models.PositiveIntegerField(blank=True, default=0)
    owner = models.ForeignKey(User, null=False, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date', )


class Rsvp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')

    def save(self, *args, **kwargs):
        self.event.participants += 1
        self.event.save()
        super(Rsvp, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.event.participants -= 1
        self.event.save()
        super(Rsvp, self).delete(using, keep_parents)

