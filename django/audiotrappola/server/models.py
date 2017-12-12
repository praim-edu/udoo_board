from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class SoundTrack(models.Model):
    starts_at = models.DateTimeField('starts at')
    ends_at = models.DateTimeField('ends at')
    file_name = models.CharField(max_length=250)
    max_volume = models.IntegerField('max volume level')
    min_volume = models.IntegerField('min volume level')

    def __str__(self):
        return self.file_name
