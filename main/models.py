from django.db import models

# Create your models here.
class SenateBills(models.Model):
    bill_number = models.IntegerField()
    date_introduced = models.CharField(max_length=255, null=True, blank=True)
    session = models.CharField(max_length=255, null=True, blank=True)
    short_title = models.TextField(null=True, blank=True)
    prime_sponsor = models.CharField(max_length=255, null=True, blank=True)
    prime_sponsor_url = models.URLField(max_length=255, null=True, blank=True)
    all_sponsors = models.TextField(max_length=255, null=True, blank=True)
    last_action = models.TextField(null=True, blank=True)
    memo_title = models.TextField(null=True, blank=True)
    memo_url = models.URLField(max_length=255, null=True, blank=True)
    bill_text = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.session + ' Senate Bill ' + str(self.bill_number)

class SenateResolutions(models.Model):
    resolution_number = models.IntegerField()
    date_introduced = models.CharField(max_length=255, null=True, blank=True)
    session = models.CharField(max_length=255, null=True, blank=True)
    short_title = models.TextField(null=True, blank=True)
    prime_sponsor = models.CharField(max_length=255, null=True, blank=True)
    prime_sponsor_url = models.URLField(max_length=255, null=True, blank=True)
    all_sponsors = models.TextField(max_length=255, null=True, blank=True)
    last_action = models.TextField(null=True, blank=True)
    memo_title = models.TextField(null=True, blank=True)
    memo_url = models.URLField(max_length=255, null=True, blank=True)
    bill_text = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.session + ' Senate Resolution ' + str(self.resolution_number)